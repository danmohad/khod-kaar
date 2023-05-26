import subprocess
from Roles import Roles

class System:
    def __init__(self):
        pass

    @staticmethod
    def execute(llm_output_) -> str:
        """Execute code contained in `llm_output_` as a shell command."""
        
        System._output(llm_output_, Roles.assistant.name)

        # Ask human for approval to continue
        input_ = System._human_in_the_loop()
        if input_ == "**STOP**":
            raise RuntimeError("Action not approved. Stopping the program.")
        elif input_ != "**CONTINUE**":
            return "Code not executed. Human in the loop says:\n" + input_

        # Parse the LLM output text for code
        llm_code_ = System._parse_output_for_code(llm_output_)

        # Complain if `llm_code_` is empty
        if llm_code_ == "":
            return "NO SHELL COMMAND RECEIVED!"
        
        # Execute `llm_code_` as a shell command
        else:
            out = subprocess.run(llm_code_, shell=True, capture_output=True, text=True).stdout

            # Add a message to let the LLM know when a 
            #  shell command that generates no stdout output is successful  
            if out == "":
                return "Shell command executed successfully. No output was generated."
        
        # Return stdout output of shell command
        return out

    @staticmethod
    def _parse_output_for_code(output_) -> str:
        """Parse the LLM's output text for code based on the `code_start_stop_substr_` keyword."""
        
        code_start_stop_substr_ = "```"

        # Check if LLM failed to include code in its output
        if code_start_stop_substr_ not in output_:
            return ""
        
        # Find the first and second instances of `code_start_stop_substr_`
        # Assume that `code_start_stop_substr_` only appears twice in each LLM output
        code_start_ = System._find_nth_substr(code_start_stop_substr_, output_, 0) + \
                            len(code_start_stop_substr_)
        code_stop_ = System._find_nth_substr(code_start_stop_substr_, output_, 1)
        
        # Return the code appearing between the instances of `code_start_stop_substr_`
        return output_[code_start_:code_stop_]

    
    @staticmethod
    def _find_nth_substr(needle_, haystack_, n):
        """Find the starting position of the `n`-th substring `needle_` in the string `haystack_`."""
        
        start = haystack_.find(needle_)
        while start >= 0 and n > 0:
            start = haystack_.find(needle_, start+len(needle_))
            n -= 1
        return start

    @staticmethod
    def _human_in_the_loop():
        """Get human approval to continue program execution. This is the only human intervention in the program."""

        human_input_ = input("Approved? y=Yes, n=No, Anything else=Feedback to LLM\n")
        if human_input_ == "y":
            return "**CONTINUE**"
        elif human_input_ == "n":
            return "**STOP**"
        else:
            return human_input_
        
    @staticmethod
    def _output(output_: str, role_: str) -> None:
        """Write `role_` and associated `output_` to console."""

        print(f'{role_}: {output_}', flush=True)