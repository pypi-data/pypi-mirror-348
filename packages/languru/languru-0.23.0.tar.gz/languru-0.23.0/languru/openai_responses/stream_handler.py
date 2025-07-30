import copy
import logging
import typing

import agents
import httpx
import logfire
import openai
from agents.run_context import RunContextWrapper, TContext
from agents.usage import Usage
from openai._types import NOT_GIVEN, Body, Headers, NotGiven, Query
from openai.types.responses import parsed_response, response_create_params
from openai.types.responses.response_audio_delta_event import ResponseAudioDeltaEvent
from openai.types.responses.response_audio_done_event import ResponseAudioDoneEvent
from openai.types.responses.response_audio_transcript_delta_event import (
    ResponseAudioTranscriptDeltaEvent,
)
from openai.types.responses.response_audio_transcript_done_event import (
    ResponseAudioTranscriptDoneEvent,
)
from openai.types.responses.response_code_interpreter_call_code_delta_event import (
    ResponseCodeInterpreterCallCodeDeltaEvent,
)
from openai.types.responses.response_code_interpreter_call_code_done_event import (
    ResponseCodeInterpreterCallCodeDoneEvent,
)
from openai.types.responses.response_code_interpreter_call_completed_event import (
    ResponseCodeInterpreterCallCompletedEvent,
)
from openai.types.responses.response_code_interpreter_call_in_progress_event import (
    ResponseCodeInterpreterCallInProgressEvent,
)
from openai.types.responses.response_code_interpreter_call_interpreting_event import (
    ResponseCodeInterpreterCallInterpretingEvent,
)
from openai.types.responses.response_completed_event import ResponseCompletedEvent
from openai.types.responses.response_computer_tool_call import ResponseComputerToolCall
from openai.types.responses.response_content_part_added_event import (
    ResponseContentPartAddedEvent,
)
from openai.types.responses.response_content_part_done_event import (
    ResponseContentPartDoneEvent,
)
from openai.types.responses.response_created_event import ResponseCreatedEvent
from openai.types.responses.response_error_event import ResponseErrorEvent
from openai.types.responses.response_failed_event import ResponseFailedEvent
from openai.types.responses.response_file_search_call_completed_event import (
    ResponseFileSearchCallCompletedEvent,
)
from openai.types.responses.response_file_search_call_in_progress_event import (
    ResponseFileSearchCallInProgressEvent,
)
from openai.types.responses.response_file_search_call_searching_event import (
    ResponseFileSearchCallSearchingEvent,
)
from openai.types.responses.response_function_call_arguments_delta_event import (
    ResponseFunctionCallArgumentsDeltaEvent,
)
from openai.types.responses.response_function_call_arguments_done_event import (
    ResponseFunctionCallArgumentsDoneEvent,
)
from openai.types.responses.response_function_tool_call import ResponseFunctionToolCall
from openai.types.responses.response_in_progress_event import ResponseInProgressEvent
from openai.types.responses.response_includable import ResponseIncludable
from openai.types.responses.response_incomplete_event import ResponseIncompleteEvent
from openai.types.responses.response_input_param import (
    ComputerCallOutput,
    FunctionCallOutput,
    ResponseInputParam,
)
from openai.types.responses.response_output_item_added_event import (
    ResponseOutputItemAddedEvent,
)
from openai.types.responses.response_output_item_done_event import (
    ResponseOutputItemDoneEvent,
)
from openai.types.responses.response_reasoning_summary_part_added_event import (
    ResponseReasoningSummaryPartAddedEvent,
)
from openai.types.responses.response_reasoning_summary_part_done_event import (
    ResponseReasoningSummaryPartDoneEvent,
)
from openai.types.responses.response_reasoning_summary_text_delta_event import (
    ResponseReasoningSummaryTextDeltaEvent,
)
from openai.types.responses.response_reasoning_summary_text_done_event import (
    ResponseReasoningSummaryTextDoneEvent,
)
from openai.types.responses.response_refusal_delta_event import (
    ResponseRefusalDeltaEvent,
)
from openai.types.responses.response_refusal_done_event import ResponseRefusalDoneEvent
from openai.types.responses.response_stream_event import ResponseStreamEvent
from openai.types.responses.response_text_annotation_delta_event import (
    ResponseTextAnnotationDeltaEvent,
)
from openai.types.responses.response_text_config_param import ResponseTextConfigParam
from openai.types.responses.response_text_delta_event import ResponseTextDeltaEvent
from openai.types.responses.response_text_done_event import ResponseTextDoneEvent
from openai.types.responses.response_web_search_call_completed_event import (
    ResponseWebSearchCallCompletedEvent,
)
from openai.types.responses.response_web_search_call_in_progress_event import (
    ResponseWebSearchCallInProgressEvent,
)
from openai.types.responses.response_web_search_call_searching_event import (
    ResponseWebSearchCallSearchingEvent,
)
from openai.types.shared_params.metadata import Metadata
from openai.types.shared_params.reasoning import Reasoning
from openai.types.shared_params.responses_model import ResponsesModel

from languru.openai_agents.messages import MessageBuilder
from languru.openai_shared.tools import function_tool_to_responses_tool_param

logger = logging.getLogger(__name__)

FAKE_ID: typing.Final = "__fake_id__"


class OpenAIResponseStreamHandler(typing.Generic[TContext]):
    def __init__(
        self,
        openai_client: openai.AsyncOpenAI,
        *,
        input: typing.Union[str, ResponseInputParam],
        model: ResponsesModel,
        include: (
            typing.Optional[typing.List[ResponseIncludable]] | NotGiven
        ) = NOT_GIVEN,
        instructions: typing.Optional[str] | NotGiven = NOT_GIVEN,
        max_output_tokens: typing.Optional[int] | NotGiven = NOT_GIVEN,
        metadata: typing.Optional[Metadata] | NotGiven = NOT_GIVEN,
        parallel_tool_calls: typing.Optional[bool] | NotGiven = NOT_GIVEN,
        previous_response_id: typing.Optional[str] | NotGiven = NOT_GIVEN,
        reasoning: typing.Optional[Reasoning] | NotGiven = NOT_GIVEN,
        service_tier: (
            typing.Optional[typing.Literal["auto", "default", "flex"]] | NotGiven
        ) = NOT_GIVEN,
        store: typing.Optional[bool] | NotGiven = NOT_GIVEN,
        temperature: typing.Optional[float] | NotGiven = NOT_GIVEN,
        text: ResponseTextConfigParam | NotGiven = NOT_GIVEN,
        tool_choice: response_create_params.ToolChoice | NotGiven = NOT_GIVEN,
        tools: (
            typing.Iterable[agents.FunctionTool] | NotGiven
        ) = NOT_GIVEN,  # Use agents.FunctionTool instead of ToolParam
        top_p: typing.Optional[float] | NotGiven = NOT_GIVEN,
        truncation: (
            typing.Optional[typing.Literal["auto", "disabled"]] | NotGiven
        ) = NOT_GIVEN,
        user: str | NotGiven = NOT_GIVEN,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        context: TContext | None = None,
        **kwargs,
    ):
        self.__openai_client = openai_client
        self.__input: ResponseInputParam = (
            [MessageBuilder.easy_input_message(content=input, role="user")]
            if isinstance(input, str)
            else copy.deepcopy(input)
        )
        self.__model = model
        self.__include = include
        self.__instructions = instructions
        self.__max_output_tokens = max_output_tokens
        self.__metadata = metadata
        self.__parallel_tool_calls = parallel_tool_calls
        self.__previous_response_id = previous_response_id
        self.__reasoning = reasoning
        self.__service_tier = service_tier
        self.__store = store
        self.__temperature = temperature
        self.__text = text
        self.__tool_choice: response_create_params.ToolChoice | NotGiven = tool_choice
        self.__tools = tools
        self.__top_p = top_p
        self.__truncation: NotGiven | typing.Literal["auto", "disabled"] | None = (
            truncation
        )
        self.__user = user
        self.__extra_headers = extra_headers
        self.__extra_query = extra_query
        self.__extra_body = extra_body
        self.__timeout = timeout

        self.__context = context
        self.__final_response: typing.Optional[parsed_response.ParsedResponse] = None

        self.__accumulated_usage = Usage()
        self.__closed = False

    async def run_until_done(self, *, limit: int = 10) -> None:
        if self.__closed:
            raise RuntimeError("Stream handler is designed to be used once")
        if limit <= 0 or limit > 25:
            raise ValueError("Limit must be between 1 and 25")

        required_action: bool = True

        current_limit = 0
        input_ = self.__input
        previous_response_id = self.__previous_response_id

        while required_action and current_limit <= limit:
            current_limit += 1

            async with self.__openai_client.responses.stream(
                input=input_,
                model=self.__model,
                tools=(
                    [
                        function_tool_to_responses_tool_param(tool)
                        for tool in self.__tools
                    ]
                    if self.__tools is not None and isinstance(self.__tools, list)
                    else NOT_GIVEN
                ),
                include=self.__include,
                instructions=self.__instructions,
                max_output_tokens=self.__max_output_tokens,
                metadata=self.__metadata,
                parallel_tool_calls=self.__parallel_tool_calls,
                previous_response_id=previous_response_id,
                reasoning=self.__reasoning,
                store=self.__store,
                temperature=self.__temperature,
                text=self.__text,
                tool_choice=self.__tool_choice,
                top_p=self.__top_p,
                truncation=self.__truncation,
                user=self.__user,
                extra_headers=self.__extra_headers,
                extra_query=self.__extra_query,
                extra_body=self.__extra_body,
                timeout=self.__timeout,
            ) as stream:
                async for event in stream:
                    await self.__on_event(event)

                await stream.until_done()

                final_response = self.__final_response = (
                    await stream.get_final_response()
                ).model_copy(deep=True)

                self.__accumulated_usage.add(
                    Usage(
                        requests=1,
                        input_tokens=(
                            final_response.usage.input_tokens
                            if final_response.usage is not None
                            else 0
                        ),
                        output_tokens=(
                            final_response.usage.output_tokens
                            if final_response.usage is not None
                            else 0
                        ),
                        total_tokens=(
                            final_response.usage.total_tokens
                            if final_response.usage is not None
                            else 0
                        ),
                    )
                )

                previous_response_id = self.__previous_response_id = final_response.id

                _required_action_calls: typing.List[
                    parsed_response.ParsedResponseFunctionToolCall
                    | ResponseComputerToolCall
                ] = []

                for output in final_response.output:
                    if output.type in (
                        "message",
                        "reasoning",
                        "web_search_call",
                        "file_search_call",
                    ):
                        pass  # No required action
                    elif output.type in (
                        "function_call",
                        "computer_call",
                    ):  # Need actions
                        _required_action_calls.append(output)  # type: ignore
                    else:
                        logger.warning(f"Unhandled response.output.type: {output.type}")

                # No required action calls, so we're done
                if len(_required_action_calls) == 0:
                    logger.info("No required action calls")
                    required_action = False

                # Required action calls, so we need to execute them
                else:
                    logger.info(f"Required action calls: {len(_required_action_calls)}")
                    required_action = True

                    for required_action_call in _required_action_calls:

                        input_: ResponseInputParam = [
                            await self.execute_required_action_call(
                                required_action_call
                            )
                        ]

        self.__closed = True

    async def execute_required_action_call(
        self,
        required_action_call: typing.Union[
            parsed_response.ParsedResponseFunctionToolCall, ResponseComputerToolCall
        ],
        **kwargs,
    ) -> typing.Union[
        ComputerCallOutput,
        FunctionCallOutput,
    ]:
        with logfire.span(f"execute_action_call:{required_action_call.call_id}"):
            if required_action_call.type == "function_call":
                return await self.execute_function_call(required_action_call, **kwargs)
            elif required_action_call.type == "computer_call":
                return await self.execute_computer_call(required_action_call, **kwargs)
            else:
                logger.error(
                    "Not implemented required action call type: "
                    + f"{required_action_call.type}"
                )
                raise ValueError(
                    "Not implemented required action call type: "
                    + f"{required_action_call.type}"
                )

    async def execute_computer_call(
        self,
        required_computer_call: ResponseComputerToolCall,
        **kwargs,
    ) -> ComputerCallOutput:
        return ComputerCallOutput(
            call_id=required_computer_call.call_id,
            output={
                "type": "computer_screenshot",
                "file_id": FAKE_ID,
                "image_url": "https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status/501",  # noqa: E501
            },
            type="computer_call_output",
        )

    async def execute_function_call(
        self,
        required_function_call: (
            parsed_response.ParsedResponseFunctionToolCall | ResponseFunctionToolCall
        ),
        **kwargs,
    ) -> FunctionCallOutput:
        with logfire.span(
            f"execute_function_call:{required_function_call.name}"
        ) as span:
            if (
                self.__tools == NOT_GIVEN
                or isinstance(self.__tools, NotGiven)
                or len(list(self.__tools)) == 0
            ):
                logger.error(
                    f"No tools provided but got tool call: {required_function_call}"
                )
                span.set_attribute("success", "false")
                span.set_attribute("error", "No tools provided")
                return FunctionCallOutput(
                    call_id=required_function_call.call_id,
                    output="Not available currently",
                    type="function_call_output",
                )

            func_tool: agents.FunctionTool
            for tool in self.__tools:
                if tool.name == required_function_call.name:
                    func_tool = tool
                    break
            else:
                logger.error(
                    f"Function tool not found: {required_function_call.name}"
                    + f", available tools: {', '.join(t.name for t in self.__tools)}"
                )
                span.set_attribute("success", "false")
                span.set_attribute("error", "Function tool not found")
                return FunctionCallOutput(
                    call_id=required_function_call.call_id,
                    output="Not available currently",
                    type="function_call_output",
                )

            try:
                func_output = await func_tool.on_invoke_tool(
                    RunContextWrapper(self.__context, self.__accumulated_usage),
                    required_function_call.arguments,
                )
                span.set_attribute("success", "true")
                return FunctionCallOutput(
                    call_id=required_function_call.call_id,
                    output=func_output,
                    type="function_call_output",
                )

            except Exception as e:
                logger.error(f"Error executing function tool: {e}")
                span.set_attribute("success", "false")
                span.set_attribute("error", "Error executing function tool")
                return FunctionCallOutput(
                    call_id=required_function_call.call_id,
                    output="Error executing function",
                    type="function_call_output",
                )

    def retrieve_final_response(self) -> parsed_response.ParsedResponse:
        if self.__final_response is None:
            raise RuntimeError("No final response")
        return self.__final_response

    async def __on_event(self, event: ResponseStreamEvent) -> None:
        await self.on_event(event)

        if event.type == "response.audio.delta":
            await self.on_response_audio_delta(event)
        elif event.type == "response.audio.done":
            await self.on_response_audio_done(event)
        elif event.type == "response.audio.transcript.delta":
            await self.on_response_audio_transcript_delta(event)
        elif event.type == "response.audio.transcript.done":
            await self.on_response_audio_transcript_done(event)
        elif event.type == "response.code_interpreter_call.code.delta":
            await self.on_response_code_interpreter_call_code_delta(event)
        elif event.type == "response.code_interpreter_call.code.done":
            await self.on_response_code_interpreter_call_code_done(event)
        elif event.type == "response.code_interpreter_call.completed":
            await self.on_response_code_interpreter_call_completed(event)
        elif event.type == "response.code_interpreter_call.in_progress":
            await self.on_response_code_interpreter_call_in_progress(event)
        elif event.type == "response.code_interpreter_call.interpreting":
            await self.on_response_code_interpreter_call_interpreting(event)
        elif event.type == "response.completed":
            await self.on_response_completed(event)
        elif event.type == "response.content_part.added":
            await self.on_response_content_part_added(event)
        elif event.type == "response.content_part.done":
            await self.on_response_content_part_done(event)
        elif event.type == "response.created":
            await self.on_response_created(event)
        elif event.type == "error":
            await self.on_response_error(event)
        elif event.type == "response.file_search_call.completed":
            await self.on_response_file_search_call_completed(event)
        elif event.type == "response.file_search_call.in_progress":
            await self.on_response_file_search_call_in_progress(event)
        elif event.type == "response.file_search_call.searching":
            await self.on_response_file_search_call_searching(event)
        elif event.type == "response.function_call_arguments.delta":
            await self.on_response_function_call_arguments_delta(event)
        elif event.type == "response.function_call_arguments.done":
            await self.on_response_function_call_arguments_done(event)
        elif event.type == "response.in_progress":
            await self.on_response_in_progress(event)
        elif event.type == "response.failed":
            await self.on_response_failed(event)
        elif event.type == "response.incomplete":
            await self.on_response_incomplete(event)
        elif event.type == "response.output_item.added":
            await self.on_response_output_item_added(event)
        elif event.type == "response.output_item.done":
            await self.on_response_output_item_done(event)
        elif event.type == "response.reasoning_summary_part.added":
            await self.on_response_reasoning_summary_part_added(event)
        elif event.type == "response.reasoning_summary_part.done":
            await self.on_response_reasoning_summary_part_done(event)
        elif event.type == "response.reasoning_summary_text.delta":
            await self.on_response_reasoning_summary_text_delta(event)
        elif event.type == "response.reasoning_summary_text.done":
            await self.on_response_reasoning_summary_text_done(event)
        elif event.type == "response.refusal.delta":
            await self.on_response_refusal_delta(event)
        elif event.type == "response.refusal.done":
            await self.on_response_refusal_done(event)
        elif event.type == "response.output_text.annotation.added":
            await self.on_response_output_text_annotation_added(event)
        elif event.type == "response.output_text.delta":
            await self.on_response_output_text_delta(event)
        elif event.type == "response.output_text.done":
            await self.on_response_output_text_done(event)
        elif event.type == "response.web_search_call.completed":
            await self.on_response_web_search_call_completed(event)
        elif event.type == "response.web_search_call.in_progress":
            await self.on_response_web_search_call_in_progress(event)
        elif event.type == "response.web_search_call.searching":
            await self.on_response_web_search_call_searching(event)
        else:
            logger.warning(f"Unhandled event type: {event.type}")

    async def on_event(self, event: ResponseStreamEvent):
        """Base handler for all events."""
        pass

    async def on_response_audio_delta(self, event: ResponseAudioDeltaEvent):
        """Handle audio delta events."""
        pass

    async def on_response_audio_done(self, event: ResponseAudioDoneEvent):
        """Handle audio done events."""
        pass

    async def on_response_audio_transcript_delta(
        self, event: ResponseAudioTranscriptDeltaEvent
    ):
        """Handle audio transcript delta events."""
        pass

    async def on_response_audio_transcript_done(
        self, event: ResponseAudioTranscriptDoneEvent
    ):
        """Handle audio transcript done events."""
        pass

    async def on_response_code_interpreter_call_code_delta(
        self, event: ResponseCodeInterpreterCallCodeDeltaEvent
    ):
        """Handle code interpreter call code delta events."""
        pass

    async def on_response_code_interpreter_call_code_done(
        self, event: ResponseCodeInterpreterCallCodeDoneEvent
    ):
        """Handle code interpreter call code done events."""
        pass

    async def on_response_code_interpreter_call_completed(
        self, event: ResponseCodeInterpreterCallCompletedEvent
    ):
        """Handle code interpreter call completed events."""
        pass

    async def on_response_code_interpreter_call_in_progress(
        self, event: ResponseCodeInterpreterCallInProgressEvent
    ):
        """Handle code interpreter call in progress events."""
        pass

    async def on_response_code_interpreter_call_interpreting(
        self, event: ResponseCodeInterpreterCallInterpretingEvent
    ):
        """Handle code interpreter call interpreting events."""
        pass

    async def on_response_completed(self, event: ResponseCompletedEvent):
        """Handle completed events."""
        pass

    async def on_response_content_part_added(
        self, event: ResponseContentPartAddedEvent
    ):
        """Handle content part added events."""
        pass

    async def on_response_content_part_done(self, event: ResponseContentPartDoneEvent):
        """Handle content part done events."""
        pass

    async def on_response_created(self, event: ResponseCreatedEvent):
        """Handle created events."""
        pass

    async def on_response_error(self, event: ResponseErrorEvent):
        """Handle error events."""
        pass

    async def on_response_file_search_call_completed(
        self, event: ResponseFileSearchCallCompletedEvent
    ):
        """Handle file search call completed events."""
        pass

    async def on_response_file_search_call_in_progress(
        self, event: ResponseFileSearchCallInProgressEvent
    ):
        """Handle file search call in progress events."""
        pass

    async def on_response_file_search_call_searching(
        self, event: ResponseFileSearchCallSearchingEvent
    ):
        """Handle file search call searching events."""
        pass

    async def on_response_function_call_arguments_delta(
        self, event: ResponseFunctionCallArgumentsDeltaEvent
    ):
        """Handle function call arguments delta events."""
        pass

    async def on_response_function_call_arguments_done(
        self, event: ResponseFunctionCallArgumentsDoneEvent
    ):
        """Handle function call arguments done events."""
        pass

    async def on_response_in_progress(self, event: ResponseInProgressEvent):
        """Handle in progress events."""
        pass

    async def on_response_failed(self, event: ResponseFailedEvent):
        """Handle failed events."""
        pass

    async def on_response_incomplete(self, event: ResponseIncompleteEvent):
        """Handle incomplete events."""
        pass

    async def on_response_output_item_added(self, event: ResponseOutputItemAddedEvent):
        """Handle output item added events."""
        pass

    async def on_response_output_item_done(self, event: ResponseOutputItemDoneEvent):
        """Handle output item done events."""
        pass

    async def on_response_reasoning_summary_part_added(
        self, event: ResponseReasoningSummaryPartAddedEvent
    ):
        """Handle reasoning summary part added events."""
        pass

    async def on_response_reasoning_summary_part_done(
        self, event: ResponseReasoningSummaryPartDoneEvent
    ):
        """Handle reasoning summary part done events."""
        pass

    async def on_response_reasoning_summary_text_delta(
        self, event: ResponseReasoningSummaryTextDeltaEvent
    ):
        """Handle reasoning summary text delta events."""
        pass

    async def on_response_reasoning_summary_text_done(
        self, event: ResponseReasoningSummaryTextDoneEvent
    ):
        """Handle reasoning summary text done events."""
        pass

    async def on_response_refusal_delta(self, event: ResponseRefusalDeltaEvent):
        """Handle refusal delta events."""
        pass

    async def on_response_refusal_done(self, event: ResponseRefusalDoneEvent):
        """Handle refusal done events."""
        pass

    async def on_response_output_text_annotation_added(
        self, event: ResponseTextAnnotationDeltaEvent
    ):
        """Handle output text annotation added events."""
        pass

    async def on_response_output_text_delta(self, event: ResponseTextDeltaEvent):
        """Handle output text delta events."""
        pass

    async def on_response_output_text_done(self, event: ResponseTextDoneEvent):
        """Handle output text done events."""
        pass

    async def on_response_web_search_call_completed(
        self, event: ResponseWebSearchCallCompletedEvent
    ):
        """Handle web search call completed events."""
        pass

    async def on_response_web_search_call_in_progress(
        self, event: ResponseWebSearchCallInProgressEvent
    ):
        """Handle web search call in progress events."""
        pass

    async def on_response_web_search_call_searching(
        self, event: ResponseWebSearchCallSearchingEvent
    ):
        """Handle web search call searching events."""
        pass

    @property
    def closed(self) -> bool:
        return self.__closed
