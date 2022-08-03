from .turboshell import ts
from .ui import print_list
from .utils import split_cmd_shortcut, write_to_file
from .vars import (
    CMD_SEP,
    FOUND_CMDS_FILE,
    LIMIT_CMD_MATCH,
)


def find_matching_commands(args, definitions, add_run_instructions):
    """
    Returns tuple of (matches, output, run)
    """
    matches = []
    output = []
    run = False
    
    def out(line=''):
        output.append(line)
    
    if len(args) >= 1:
        cmd = args[0]
        if add_run_instructions:
            run = not cmd.endswith(".")
        cmd_chunks = split_cmd_shortcut(args[0])
        if len(cmd_chunks) > 0:
            _find_matches(matches, cmd_chunks, definitions)
            write_to_file(FOUND_CMDS_FILE, matches[:LIMIT_CMD_MATCH])
            _build_output(matches, out, run, add_run_instructions)
        else:
            out(f"Can only match command with '{CMD_SEP}' in name.")
    else:
        out("No command name supplied")
    return matches, output, run


def _find_matches(matches, cmd_chunks, definitions):
    chunk_count = len(cmd_chunks)
    for line in definitions:
        line_chunks = line.split(CMD_SEP)
        if len(line_chunks) < chunk_count:
            continue
        chunk_match = 0
        for cmd_chunk, line_chunk in zip(cmd_chunks, line_chunks):
            if not line_chunk.startswith(cmd_chunk):
                continue
            chunk_match += 1
        if chunk_match == chunk_count:
            matches.append(line.strip())


def _dont_run_in_subshell(match):
    """
    Returns True if command should not be run in a subshell, typically because
    we want the effect to apply to the current shell. 
    So things like "cd" or "source" etc...
    """
    return match in ts.no_subshell or match.startswith('cd.') or match.endswith('.cd')


def _build_output(matches, out, run, add_run_instructions):
    match_count = len(matches)
    if match_count == 0:
        out("Found 0 matches.")
    elif match_count == 1:
        match = matches[0]
        if _dont_run_in_subshell(match):
            out("Found a single match:")
            out("")
            out(f"    1 - {match}")
            out("")
            if add_run_instructions:
                out("But running it in a sub shell won't work.")
                out("Type 1 to run it in the current shell.")
        else:
            if run:
                out(match)
            else:
                out("Found a single match:")
                out("")
                out(f"    1 - {match}")
                out("")
                # This line must contain spaces!
                out("(Not running match as this is search mode)")
    elif match_count > 1:
        out("Turboshell found multiple matches:")
        out()
        print_list(matches, 1, LIMIT_CMD_MATCH, out)
        out()
        if match_count > LIMIT_CMD_MATCH:
            out(f"Found {match_count - LIMIT_CMD_MATCH} more matches not shown.")
            out()
        if add_run_instructions:
            out('Type the number of the command you want to run.')
