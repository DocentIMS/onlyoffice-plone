## How to give me commands

- Always give me COMPLETE, copy-pasteable commands. No "type this then add the path."
- If you need a value (domain, IP, path, port, username, password file location, etc.), ASK ME FIRST, then build the fully-filled-in command. Never use `<placeholders>`.
- Do not split a single operation across multiple terminal windows without saying explicitly which window each command goes in. Default: assume I have one terminal open.
- Default OS: Windows. Default shell on laptop: MobaXterm local terminal. Windows drives are mounted at `/drives/c/...` — never `/c/`, never `/cygdrive/c/`.
- When editing a file on a server, prefer "send me the whole patched file, I scp it" over "edit these lines in nano." Nano edits with paste corrupt easily.
- After a multi-step sequence, end with one verification step (e.g., "if you see X you're good").
- If I'm pasting and it breaks (paste turns `>` into `.`, `>` into nothing, etc.), the fix is on YOU to find a paste-free alternative, not to lecture me.
