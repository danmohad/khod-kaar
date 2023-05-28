import os
import subprocess
from colorama import Fore
from colorama import Back
from colorama import Style

class System:
    def __init__(self):
        
        # Keep track of the current working directory
        self.cwd = os.getcwd()

    def execute(self, llm_output_) -> str:
        """Execute code contained in `llm_output_` as a shell command."""

        # Ask human for approval to continue
        input_ = System._human_in_the_loop()
        if input_ == "**STOP**":
            raise RuntimeError("Action not approved. Stopping the program.")
        elif input_ != "**CONTINUE**":
            return "Code not executed. Human in the loop says:\n" + input_

        # Parse the LLM output text for code
        llm_code_ = System._parse_output_for_code(llm_output_)

        # Complain if `llm_code_` is empty and return
        if llm_code_ == "":
            return "NO SHELL COMMAND RECEIVED!"

        # Append cwd check to code to keep track of it
        split_kwd = "**PWD**"
        llm_code_ += f" && echo '{split_kwd}' && pwd"

        # Execute `llm_code_` as a shell command
        out = subprocess.run(llm_code_, 
            shell=True, capture_output=True, text=True, cwd=self.cwd).stdout

        # Parse the cwd from the output
        out, cwd_ = out.split(split_kwd)
        self.cwd = "".join(cwd_.split())
        
        # Add a message to let the LLM know when a 
        #  shell command that generates no stdout output is successful  
        if out == "" or out.isspace():
            out = "Shell command executed successfully. No output was generated."

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
        # TODO Make sure to take the last two substrings, since sometimes it writes the "code"
            # and then write the bash commands to "write" the code
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

        print("")
        human_input_ = input(f"Approved? {Back.GREEN}y=Yes{Style.RESET_ALL}, {Back.RED}n=No{Style.RESET_ALL}, Anything else=Feedback to LLM\n")
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