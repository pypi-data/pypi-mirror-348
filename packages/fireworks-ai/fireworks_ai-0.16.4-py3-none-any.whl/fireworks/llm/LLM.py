from collections import defaultdict, deque
from datetime import timedelta
import inspect
import time
from fireworks.client.api_client import FireworksClient
from fireworks.client.chat import Chat as FireworksChat
from fireworks.client.chat_completion import ChatCompletionV2 as FireworksChatCompletion
from asyncstdlib.functools import cache
from functools import cache as sync_cache
from typing import (
    AsyncGenerator,
    Generator,
    Iterable,
    Literal,
    Optional,
    Union,
    overload,
)
from fireworks.client.error import BadGatewayError, ServiceUnavailableError
from fireworks.gateway import Gateway
from fireworks.control_plane.generated.protos.gateway import (
    AcceleratorType as AcceleratorTypeEnum,
    AutoscalingPolicy,
    DeployedModelState,
    Deployment,
    DeploymentState,
    Model,
)
import asyncio
import logging
import os
import atexit
from openai.types.chat.chat_completion import ChatCompletion as OpenAIChatCompletion
from openai.types.chat.chat_completion_chunk import ChatCompletionChunk
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam
from openai.types.chat.completion_create_params import ResponseFormat
from openai import NOT_GIVEN, NotGiven
from fireworks._util import run_coroutine_in_appropriate_loop
import sysconfig

# Configure logger with a consistent format for better debugging
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.propagate = False  # Prevent duplicate logs

if os.environ.get("FIREWORKS_SDK_DEBUG"):
    logger.setLevel(logging.DEBUG)


ReasoningEffort = Literal["low", "medium", "high"]


class ChatCompletion:
    def __init__(self, llm: "LLM"):
        self._client = FireworksChatCompletion(llm._client)
        self._llm = llm

    @overload
    def create(
        self,
        messages: Iterable[ChatCompletionMessageParam],
        stream: Literal[False] = False,
        response_format: Optional[ResponseFormat] = None,
        reasoning_effort: Optional[ReasoningEffort] = None,
        max_tokens: Optional[int] = None,
        extra_headers=None,
        **kwargs,
    ) -> OpenAIChatCompletion:
        pass

    @overload
    def create(
        self,
        messages: Iterable[ChatCompletionMessageParam],
        stream: Literal[True] = True,
        response_format: Optional[ResponseFormat] = None,
        reasoning_effort: Optional[ReasoningEffort] = None,
        max_tokens: Optional[int] = None,
        extra_headers=None,
        **kwargs,
    ) -> Generator[ChatCompletionChunk, None, None]:
        pass

    def create(
        self,
        messages: Iterable[ChatCompletionMessageParam],
        stream: bool = False,
        response_format: Optional[ResponseFormat] = None,
        reasoning_effort: Optional[ReasoningEffort] = None,
        max_tokens: Optional[int] = None,
        extra_headers=None,
        **kwargs,
    ) -> Union[OpenAIChatCompletion, Generator[ChatCompletionChunk, None, None]]:
        """
        WARNING: Due to the need to run a coroutine in an event loop, only use
        this method in a sync context. In general, we recommend using the async
        version of this method, acreate.
        """
        run_coroutine_in_appropriate_loop(self._llm._ensure_deployment_ready())
        model_id = run_coroutine_in_appropriate_loop(self._llm.model_id())
        retries = 0
        while retries < self._llm.max_retries:
            try:
                if self._llm.enable_metrics:
                    start_time = time.time()
                result = self._client.create(
                    model=model_id,
                    prompt_or_messages=messages,
                    stream=stream,
                    extra_headers=extra_headers,
                    response_format=response_format,
                    reasoning_effort=reasoning_effort,
                    max_tokens=max_tokens,
                    **kwargs,
                )
                if self._llm.enable_metrics:
                    end_time = time.time()
                    self._llm._metrics.add_metric("time_to_last_token", end_time - start_time)
                return result
            except BadGatewayError:
                retries += 1
            except ServiceUnavailableError:
                retries += 1
        raise Exception(f"Failed to create chat completion after {self._llm.max_retries} retries")

    @overload
    async def acreate(
        self,
        messages: Iterable[ChatCompletionMessageParam],
        stream: Literal[False] = False,
        response_format: Optional[ResponseFormat] = None,
        reasoning_effort: Optional[ReasoningEffort] = None,
        max_tokens: Optional[int] = None,
        extra_headers=None,
        **kwargs,
    ) -> OpenAIChatCompletion: ...

    @overload
    async def acreate(
        self,
        messages: Iterable[ChatCompletionMessageParam],
        stream: Literal[True] = True,
        response_format: Optional[ResponseFormat] = None,
        reasoning_effort: Optional[ReasoningEffort] = None,
        max_tokens: Optional[int] = None,
        extra_headers=None,
        **kwargs,
    ) -> AsyncGenerator[ChatCompletionChunk, None]:
        pass

    async def acreate(
        self,
        messages: Iterable[ChatCompletionMessageParam],
        stream: bool = False,
        response_format: Optional[ResponseFormat] = None,
        reasoning_effort: Optional[ReasoningEffort] = None,
        max_tokens: Optional[int] = None,
        extra_headers=None,
        **kwargs,
    ) -> Union[OpenAIChatCompletion, AsyncGenerator[ChatCompletionChunk, None]]:
        await self._llm._ensure_deployment_ready()
        model_id = await self._llm.model_id()
        retries = 0
        while retries < self._llm.max_retries:
            try:
                resp_or_generator = self._client.acreate(  # type: ignore
                    model=model_id,
                    prompt_or_messages=messages,
                    stream=stream,
                    extra_headers=extra_headers,
                    response_format=response_format,
                    reasoning_effort=reasoning_effort,
                    max_tokens=max_tokens,
                    **kwargs,
                )
                if stream:
                    return resp_or_generator  # type: ignore
                else:
                    if self._llm.enable_metrics:
                        start_time = time.time()
                    resp = await resp_or_generator  # type: ignore
                    if self._llm.enable_metrics:
                        end_time = time.time()
                        self._llm._metrics.add_metric("time_to_last_token", end_time - start_time)
                    return resp
            except BadGatewayError as e:
                logger.debug(f"BadGatewayError: {e}. model_id: {model_id}")
                retries += 1
            except ServiceUnavailableError as e:
                logger.debug(f"ServiceUnavailableError: {e}. model_id: {model_id}")
                retries += 1
        raise Exception(f"Failed to create chat completion after {self._llm.max_retries} retries")


class Chat:
    def __init__(self, llm: "LLM", model):
        self.completions = ChatCompletion(llm)


# Make param a literal type so developer does not need to import AcceleratorType enum
AcceleratorTypeLiteral = Literal[
    "NVIDIA_A100_80GB",
    "NVIDIA_H100_80GB",
    "AMD_MI300X_192GB",
    "NVIDIA_A10G_24GB",
    "NVIDIA_A100_40GB",
    "NVIDIA_L4_24GB",
    "NVIDIA_H200_141GB",
    "NVIDIA_B200_180GB",
]


DEFAULT_MAX_RETRIES = 3


class Metrics:
    """
    A class for tracking and analyzing performance metrics for LLM operations.

    This class maintains a rolling window of metrics such as response times,
    token generation speeds, and other performance indicators. It provides
    statistical methods to analyze these metrics (mean, median, min, max).

    Each metric is stored as a list of values with a maximum size to prevent
    unbounded memory growth. When the maximum size is reached, the oldest
    values are removed in a FIFO manner.
    """

    def __init__(self, max_metrics: int = 1000):
        """
        Initialize the metrics tracker.

        Args:
            max_metrics: Maximum number of values to store for each metric.
                         Defaults to 1000. When exceeded, oldest values are removed.
        """
        self._metrics = defaultdict(deque)
        self._max_metrics = max_metrics

    def add_metric(self, metric_name: str, metric_value: float):
        """
        Add a new metric value to the specified metric.

        Args:
            metric_name: Name of the metric to track
            metric_value: Value to add to the metric
        """
        self._metrics[metric_name].append(metric_value)
        if len(self._metrics[metric_name]) > self._max_metrics:
            self._metrics[metric_name].popleft()

    def get_metric(self, metric_name: str):
        """
        Get all recorded values for a specific metric.

        Args:
            metric_name: Name of the metric to retrieve

        Returns:
            List of metric values or None if the metric doesn't exist
        """
        if metric_name not in self._metrics:
            return None
        return self._metrics[metric_name]

    def get_metric_mean(self, metric_name: str) -> Optional[float]:
        """
        Calculate the arithmetic mean of a metric's values.

        Args:
            metric_name: Name of the metric

        Returns:
            Mean value or None if the metric doesn't exist
        """
        if metric_name not in self._metrics:
            return None
        return sum(self._metrics[metric_name]) / len(self._metrics[metric_name])

    def get_metric_median(self, metric_name: str):
        """
        Calculate the median value of a metric.

        Args:
            metric_name: Name of the metric

        Returns:
            Median value or None if the metric doesn't exist
        """
        if metric_name not in self._metrics:
            return None
        return sorted(self._metrics[metric_name])[len(self._metrics[metric_name]) // 2]

    def get_metric_min(self, metric_name: str):
        """
        Get the minimum value recorded for a metric.

        Args:
            metric_name: Name of the metric

        Returns:
            Minimum value or None if the metric doesn't exist
        """
        if metric_name not in self._metrics:
            return None
        return min(self._metrics[metric_name])

    def get_metric_max(self, metric_name: str):
        """
        Get the maximum value recorded for a metric.

        Args:
            metric_name: Name of the metric

        Returns:
            Maximum value or None if the metric doesn't exist
        """
        if metric_name not in self._metrics:
            return None
        return max(self._metrics[metric_name])


class DeploymentWithIdAndName(Deployment):
    def __init__(self, deployment: Deployment, gateway: Gateway):
        self.id = deployment.name
        self.name = deployment.display_name
        self._gateway = gateway


class LLM:
    def __init__(
        self,
        model: str,
        name: Optional[str] = None,
        api_key: Optional[str] = None,
        base_url: str = "https://api.fireworks.ai/inference/v1",
        deployment_type: Literal["serverless", "on-demand"] = "serverless",
        accelerator_type: Union[AcceleratorTypeLiteral, NotGiven] = NOT_GIVEN,
        scale_up_window: timedelta = timedelta(seconds=1),
        scale_down_window: timedelta = timedelta(minutes=1),
        scale_to_zero_window: timedelta = timedelta(minutes=5),
        enable_metrics: bool = False,
        max_retries: int = DEFAULT_MAX_RETRIES,
    ):
        """
        Initialize the LLM.

        Args:
            model: The model to use.
            api_key: The API key to use.
            base_url: The base URL to use.
            deployment_type: The deployment type to use.
            accelerator_type: The accelerator type to use.
            scale_up_window: The scale up window to use.
            scale_down_window: The scale down window to use.
            scale_to_zero_window: The scale to zero window to use.
            enable_metrics: Whether to enable metrics. Only records time to last token for non-streaming requests.
                TODO: add support for streaming requests.
                TODO: add support for more metrics (TTFT, Tokens/second)
            max_retries: The maximum number of retries to use.
        """
        if not model:
            raise ValueError("model is required")
        self._client = FireworksClient(api_key=api_key, base_url=base_url)
        if name is not None and name == "":
            raise ValueError("name must be non-empty")
        self._name = name
        self._model = model
        self.chat = Chat(self, self.model)
        self.deployment_type = deployment_type
        self.max_retries = max_retries
        self.enable_metrics = enable_metrics
        self._gateway = Gateway(api_key=api_key)
        self._metrics = Metrics()
        # Add a lock to prevent concurrent calls to _ensure_deployment_ready
        self._deployment_lock = asyncio.Lock()
        atexit.register(self._gateway._channel.close)

        if isinstance(accelerator_type, str):
            self._accelerator_type = AcceleratorTypeEnum.from_string(accelerator_type)
            self._validate_model_for_gpu(self.model, self._accelerator_type)
        else:
            self._accelerator_type = accelerator_type

        # aggressive defaults for experimentation to save on cost
        self._autoscaling_policy: AutoscalingPolicy = AutoscalingPolicy(
            scale_up_window=scale_up_window,
            scale_down_window=scale_down_window,
            scale_to_zero_window=scale_to_zero_window,
        )

    @property
    def model(self):
        if not self._model.startswith("accounts/fireworks/models/"):
            return f"accounts/fireworks/models/{self._model}"
        return self._model

    @staticmethod
    def _validate_model_for_gpu(model: str, accelerator_type: AcceleratorTypeEnum):
        """
        Models are not always supported on all GPU types. This function checks if the model is supported on a GPU.
        """
        if "qwen3-1p7b" in model:
            supported_accelerators = [
                AcceleratorTypeEnum.NVIDIA_H100_80GB,
                AcceleratorTypeEnum.NVIDIA_H200_141GB,
            ]
            if accelerator_type not in supported_accelerators:
                raise ValueError(
                    f"Qwen3-1p7b is not supported on {accelerator_type}. "
                    f"Please pass one of the following accelerators: {list(map(str, supported_accelerators))} "
                    f"to the LLM constructor using the accelerator_type parameter.\n\n"
                    f"Example:\n"
                    f"    from fireworks import LLM\n"
                    f"    llm = LLM(\n"
                    f'        model="qwen3-1p7b",\n'
                    f'        accelerator_type="NVIDIA_H100_80GB"\n'
                    f"    )"
                )

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._gateway.__aexit__(exc_type, exc_val, exc_tb)

    @property
    def name(self) -> str:
        return self._get_deployment_name()

    @sync_cache
    def _get_deployment_name(self):
        if self._name is None:
            # Get fireworks package path and Python stdlib path
            import fireworks

            package_path = os.path.dirname(fireworks.__file__)
            stdlib_path = sysconfig.get_path("stdlib")

            stack = inspect.stack()
            for frame_info in stack:
                filename = frame_info.filename
                # Skip frames from our package, Python stdlib, other libraries, and internal Python
                if (
                    not filename.startswith(package_path)
                    and not filename.startswith(stdlib_path)
                    and not "/site-packages/" in filename
                    and not filename.startswith("<")
                ):
                    logger.debug(f"Found caller outside of library code to generate name: {filename}")
                    return os.path.basename(filename)
            raise ValueError("No caller found outside of library code")
        return self._name

    async def apply(self):
        """
        Like Terraform apply, this will ensure the deployment is ready and return the deployment.
        """
        await self._ensure_deployment_ready()
        return self

    def get_time_to_last_token_mean(self) -> Optional[float]:
        """
        Returns the mean time to last token for non-streaming requests. If no metrics are available, returns None.
        """
        if not self.enable_metrics:
            raise ValueError("Metrics are not enabled for this LLM")
        return self._metrics.get_metric_mean("time_to_last_token")

    async def is_available_on_serverless(self):
        """
        Checks if the model is available on serverless.
        """
        return await self._is_available_on_serverless()

    async def deployment_strategy(self) -> Literal["serverless", "on-demand"]:
        return await self._deployment_strategy()

    @cache
    async def _deployment_strategy(self) -> Literal["serverless", "on-demand"]:
        """
        Determines whether to use serverless or dedicated deployment based on model availability
        and configured deployment type.

        Returns:
            bool: True if a dedicated deployment is needed, False if serverless can be used.
        """
        if await self.is_available_on_serverless():
            if self.deployment_type == "serverless":
                logger.debug(f"Model {self.model} is available on serverless, using serverless deployment")
                return "serverless"
            else:
                logger.debug(
                    f"Model {self.model} is available on serverless, but deployment_type is on-demand, continuing to ensure deployment is ready"
                )
                return "on-demand"
        else:
            logger.debug(
                f"Model {self.model} is not available on serverless, continuing to check for existing deployment"
            )
            return "on-demand"

    @cache
    async def _is_available_on_serverless(self):
        logger.debug(f"Checking if {self.model} is available on serverless")
        models = await self._gateway.list_models(parent="accounts/fireworks", include_deployed_model_refs=True)

        # find model in models
        model = next((m for m in models if m.name == self.model), None)
        if model is None:
            raise ValueError(
                f"Model {self.model} not available on Fireworks. See https://fireworks.ai/models for available models."
            )
        logger.debug(f"Found model {self.model} on under fireworks account")
        is_serverless = self._is_model_on_serverless_account(model)
        logger.debug(f"Model {self.model} is {'serverless' if is_serverless else 'not serverless'}")
        return is_serverless

    @staticmethod
    def _is_model_on_serverless_account(model: Model) -> bool:
        """
        Check if the model is deployed on a serverless-enabled account.

        Args:
            model: The model object to check

        Returns:
            bool: True if the model is deployed on a supported serverless account, False otherwise
        """
        if model.deployed_model_refs:
            for ref in model.deployed_model_refs:
                if (
                    hasattr(ref, "state")
                    and (ref.state == DeployedModelState.DEPLOYED or ref.state == "DEPLOYED")
                    and hasattr(ref, "deployment")
                    and ref.deployment
                ):
                    # Check if deployment is on a supported account
                    if (
                        ref.deployment.startswith("accounts/fireworks/")
                        or ref.deployment.startswith("accounts/yi-01-ai/")
                        or ref.deployment.startswith("accounts/sentientfoundation/")
                    ):
                        return True
        return False

    async def _query_existing_deployment(self):
        """
        Queries all deployments for the same model and accelerator type (if given) and returns the first one.
        """
        deployments = await self._gateway.list_deployments(
            filter=f'display_name="{self.name}" AND base_model="{self.model}"'
        )
        deployment = next(iter(deployments), None)
        return deployment

    async def _ensure_deployment_ready(self) -> None:
        """
        If a deployment is inferred for this LLM, ensure it's deployed and
        ready. A deployment is required if the model is not available on
        serverless or this LLM has deployment_type="on-demand".

        This method uses a lock to prevent concurrent calls from multiple coroutines.
        """
        # Use the lock to prevent concurrent calls to this method
        async with self._deployment_lock:
            deployment_strategy = await self.deployment_strategy()
            if deployment_strategy == "serverless":
                return

            deployment = await self._query_existing_deployment()

            if deployment is None:
                logger.debug(f"No existing deployment found, creating deployment for {self.model}")
                deployment = await self._gateway.create_deployment(
                    self.name, self.model, self._autoscaling_policy, self._accelerator_type
                )
                logger.debug(f"Deployment {deployment.name} created, waiting for it to be ready")

                # poll deployment status until it's ready
                start_time = asyncio.get_event_loop().time()
                last_log_time = 0
                while deployment.state != DeploymentState.READY:
                    current_time = asyncio.get_event_loop().time()
                    # wait for 1 second
                    await asyncio.sleep(1)
                    deployment = await self._gateway.get_deployment(deployment.name)
                    if current_time - last_log_time >= 10:
                        elapsed_so_far = current_time - start_time
                        logger.debug(
                            f"Waiting for deployment {deployment.name} to be ready, current state: {deployment.state}, elapsed time: {elapsed_so_far:.2f}s"
                        )
                        last_log_time = current_time

                total_time = asyncio.get_event_loop().time() - start_time
                logger.debug(
                    f"Deployment {deployment.name} is ready, using deployment (ready in {total_time:.2f} seconds)"
                )
            else:
                logger.debug(f"Deployment {deployment.name} already exists, checking if it needs to be scaled up")

                updates = {}

                # if autoscaling policy is not equal, update it
                if not self._is_autoscaling_policy_equal(deployment):
                    logger.debug(
                        f"Updating autoscaling policy for {deployment.name} to "
                        f"{self._autoscaling_policy.scale_up_window.total_seconds()}s up, "
                        f"{self._autoscaling_policy.scale_down_window.total_seconds()}s down, "
                        f"{self._autoscaling_policy.scale_to_zero_window.total_seconds()}s to zero"
                    )
                    updates["autoscaling_policy"] = self._autoscaling_policy

                if deployment.accelerator_type != self._accelerator_type and self._accelerator_type is not NOT_GIVEN:
                    raise ValueError(
                        f'Deployment with name "{deployment.name}" has accelerator type {deployment.accelerator_type}, ',
                        f"but the LLM has accelerator type {self._accelerator_type}. You must specify a different name ",
                        f"for this LLM to use a different accelerator type since it is not possible to change the accelerator ",
                        f"type of an existing deployment.",
                    )

                if len(updates) > 0:
                    logger.debug(f"Updating deployment {deployment.name} with {updates}")
                    start_time = asyncio.get_event_loop().time()
                    await self._gateway.update_deployment(deployment.name, **updates)

                    # poll until deployment is ready
                    while deployment.state != DeploymentState.READY:
                        await asyncio.sleep(1)
                        deployment = await self._gateway.get_deployment(deployment.name)

                    elapsed_time = asyncio.get_event_loop().time() - start_time
                    logger.debug(f"Deployment update completed in {elapsed_time:.2f} seconds")

                if deployment.replica_count == 0:
                    logger.debug(f"Deployment {deployment.name} is not ready, scaling to 1 replica")
                    start_time = asyncio.get_event_loop().time()
                    await self._gateway.scale_deployment(deployment.name, 1)

                    # Poll until deployment has at least one replica
                    last_log_time = 0
                    while deployment.replica_count == 0:
                        current_time = asyncio.get_event_loop().time()
                        await asyncio.sleep(1)
                        deployment = await self._gateway.get_deployment(deployment.name)
                        if current_time - last_log_time >= 10:
                            elapsed_so_far = current_time - start_time
                            logger.debug(
                                f"Waiting for deployment {deployment.name} to scale up, current replicas: {deployment.replica_count}, elapsed time: {elapsed_so_far:.2f}s"
                            )
                            last_log_time = current_time

                    total_scale_time = asyncio.get_event_loop().time() - start_time
                    logger.debug(f"Deployment {deployment.name} scaled up in {total_scale_time:.2f} seconds")
                logger.debug(f"Deployment {deployment.name} is ready, using deployment")

    async def scale_to_zero(self) -> Optional[Deployment]:
        """
        Sends a request to scale the deployment to 0 replicas but does not wait for it to complete.
        """
        deployment = await self.deployment()
        if deployment is None:
            return None
        await self._gateway.scale_deployment(deployment.name, 0)
        return deployment

    async def scale_to_1_replica(self):
        """
        Scales the deployment to at least 1 replica.
        """
        deployment = await self.deployment()
        if deployment is None:
            return
        await self._gateway.scale_deployment(deployment.name, 1)

    def _is_autoscaling_policy_equal(self, deployment: Deployment) -> bool:
        return (
            deployment.autoscaling_policy.scale_up_window == self._autoscaling_policy.scale_up_window
            and deployment.autoscaling_policy.scale_down_window == self._autoscaling_policy.scale_down_window
            and deployment.autoscaling_policy.scale_to_zero_window == self._autoscaling_policy.scale_to_zero_window
        )

    async def deployment(self) -> Optional[DeploymentWithIdAndName]:
        return await self._deployment()

    @cache
    async def _deployment(self) -> Optional[DeploymentWithIdAndName]:
        """
        Queries for any deployment that should exist for this LLM under this
        Fireworks account. If no deployment is found, but should exist, it will
        be created and returned. If no deployment is found and should not exist,
        None is returned.
        """
        await self._ensure_deployment_ready()
        deployment = await self._query_existing_deployment()
        return DeploymentWithIdAndName(deployment, self._gateway) if deployment else None

    async def model_id(self):
        """
        Returns the model ID, which is the model name plus the deployment name
        if it exists. This is used for the "model" arg when calling the model.
        """
        if await self.is_available_on_serverless():
            return self.model
        deployment = await self.deployment()
        if deployment is None:
            return self.model
        return f"{self.model}#{deployment.id}"

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"LLM(model={self.model})"
