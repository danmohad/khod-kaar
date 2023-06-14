import os
import subprocess
import tempfile
import time
from colorama import Fore
from colorama import Back
from colorama import Style

class System:
    def __init__(self, autopilot_: bool):
        
        # Keep track of the current working directory
        self.cwd = os.getcwd()
        self._autopilot = autopilot_
        self.split_kwd = "**PWD**"

    def _prepare_command(self, llm_code: str) -> str:

        # TODO This results in "literal" \n: echo "requests\nbeautifulsoup4\npandas" > requirements2.txt. That's a problem.

        # Append cwd check to code to keep track of it
        llm_code_ += f"\necho '{self.split_kwd}'\npwd"

        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            temp_file.write(llm_code_)
            temp_file_path = temp_file.name

        return temp_file_path
    
    def execute(self, llm_output_) -> str:
        """Execute code contained in `llm_output_` as a shell command."""

        # Ask human for approval to continue
        # If LLM wants to stop and human wants to stop, both **STOP** and **CONTINUE** have the same effect
        # If LLM wants to stop but human wants to continue, human can give feedback like "you're not done yet"
        input_ = self._human_in_the_loop()
        if input_ == "**STOP**":
            return "**STOP**"
        elif input_ != "**CONTINUE**":
            return "Code not executed. Human in the loop says:\n" + input_

        # Check if LLM wants to stop execution
        if "**STOP**" in llm_output_:
            return "**STOP**"

        # Parse the LLM output text for code
        llm_code_ = System._parse_output_for_code(llm_output_)

        # TODO change this to _parse_output_for_code raising errors and excepting them here
        # Complain if `llm_code_` is empty and return
        if llm_code_ == "**NO CODE BLOCK**":
            return "No shell command received. Nothing to execute."
        elif llm_code_ == "**MULTIPLE CODE BLOCKS**":
            return "Multiple code blocks received. Only one code block can be provided at a time."

        temp_file_path = self._prepare_command(llm_code_)

        # Execute `llm_code_` as a shell command, capture any errors in execution
        try:
            sp = subprocess.run(['bash', temp_file_path],
                       check=True, capture_output=True, text=True, cwd=self.cwd)
            # When a command fails, sometimes the exit code is still 0 and subprocess doesn't raise an error because the final "pwd" command succeeds. In these cases, stderr will be non-empty.
            if sp.stderr:
                raise ValueError
            else:
                out = sp.stdout
        except subprocess.CalledProcessError as e:
            out = f"Shell command exited with status {e.returncode}"
            out += f"\nCommand was: {e.cmd}"
            out += f"\nstdout was: {e.stdout}"
            if e.stderr:
                out += f"\nstderr was: {e.stderr}"
            # Assumes that if there was a directory change in the command, it can be safely ignored, and that the LLM won't assume that the directory change took place, even if it succeeded before the part of the command that failed
            return out
        except ValueError:
            out = f"Shell command wrote to stderr"
            # out += f"\nCommand was: {sp.cmd}" # TODO parse this from the temporary file
            out += f"\nstdout was: {sp.stdout}" # might be unnecessary to output stdout, and might be confusing since contains the echo and pwd commands
            out += f"\nstderr was: {sp.stderr}"
            return out
        finally:
            os.remove(temp_file_path)

        # Parse the cwd from the output
        out, cwd_ = out.split(self.split_kwd)
        self.cwd = "".join(cwd_.split())
        
        # Add a message to let the LLM know when a shell command that generates no stdout output is successful  
        if out == "" or out.isspace():
            out = "Shell command executed successfully. No output was generated."

        # Return stdout output of shell command
        return out

    @staticmethod
    def _parse_output_for_code(output_) -> str:
        """Parse the LLM's output text for code based on the `code_start_stop_substr_` keyword."""
        
        code_start_stop_substr_ = "```"

        # Check if LLM failed to include code in its output
        count_ = System._count_substr(code_start_stop_substr_, output_)
        if count_ == 0:
            return "**NO CODE BLOCK**"
        elif count_ > 2:
            return "**MULTIPLE CODE BLOCKS**"
        
        # Find the first and second instances of `code_start_stop_substr_`
        code_start_ = System._find_nth_substr(code_start_stop_substr_, output_, 0) + \
                            len(code_start_stop_substr_)
        code_stop_ = System._find_nth_substr(code_start_stop_substr_, output_, 1)
        
        # Return the code appearing between the instances of `code_start_stop_substr_`
        code_ = output_[code_start_:code_stop_]

        # Deal with the LLM sometimes starting code with "```bash", assuming "bash" only appears once with no flags e.g. `-c`.
        code_ = code_.split("bash\n")[-1]
        return code_

    @staticmethod
    def _count_substr(needle_: str, haystack_: str) -> int:
        """Count how many `needle_` substrings there are in `haystack_`."""

        n = 0
        start = haystack_.find(needle_)
        while start >= 0:
            start = haystack_.find(needle_, start+len(needle_))
            n += 1
        return n

    @staticmethod
    def _find_nth_substr(needle_, haystack_, n):
        """Find the starting position of the `n`-th substring `needle_` in the string `haystack_`."""
        
        start = haystack_.find(needle_)
        while start >= 0 and n > 0:
            start = haystack_.find(needle_, start+len(needle_))
            n -= 1
        return start

    def _human_in_the_loop(self):
        """Get human approval to continue program execution. This is the only human intervention in the program."""

        # TODO change these returns to enumerated types
        print("")
        if self._autopilot:
            print(f"{Back.GREEN}Approved on autopilot{Style.RESET_ALL}")
            return "**CONTINUE**"

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
