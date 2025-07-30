
ZSH_AUTOCOMPLETE_TEMPLATE = """
#compdef {alias}

local curcontext="$curcontext" state line
local -a completions options described
local all_described=1

# current-2 because indexes start from 1 and need to remove tool name from start
completions=("${{(@f)$({alias} --shell-completion "$((CURRENT-2))" "${{words[@]:1}}")}}")
completions=(${{completions:#}})
(( $#completions )) || return

if [[ "${{completions[1]}}" == "__files__" ]]; then
  _files
  return
fi

local opt desc
for line in "${{completions[@]}}"; do
  opt="${{line%%$'\\t'*}}"
  desc="${{line#*$'\\t'}}"
  if [[ "$opt" == "$desc" ]]; then
    desc=""
    all_described=0
  fi
  options+=("$opt")
  described+=("$opt:$desc")
done

options=(${{options:#}})

if (( all_described )); then
  described=(${{described:#}})
  _describe -V petcmd described
elif (( ${{#options[@]}} )); then
  compadd -V petcmd -a options
fi
""".lstrip()
