_genwal_completions()
{
    local cur prev words cword
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    cword="$COMP_CWORD"
    words=("${COMP_WORDS[@]}")

    local cmd="${words[1]:-}"
    local subcmd="${words[2]:-}"

    # Level 1: top-level commands
    if [ "$cword" -eq 1 ]; then
        COMPREPLY=( $(compgen -W "run preview theme config schedule providers history seed palette doctor logs status uninstall" -- "$cur") )
        return 0
    fi

    # Level 2: subcommands
    if [ "$cword" -eq 2 ]; then
        case "$cmd" in
            theme)    COMPREPLY=( $(compgen -W "list use edit" -- "$cur") ) ;;
            config)   COMPREPLY=( $(compgen -W "edit get set" -- "$cur") ) ;;
            schedule) COMPREPLY=( $(compgen -W "set list show remove" -- "$cur") ) ;;
            history)  COMPREPLY=( $(compgen -W "list apply" -- "$cur") ) ;;
            providers) COMPREPLY=( $(compgen -W "list" -- "$cur") ) ;;
            palette)  COMPREPLY=( $(compgen -W "preview" -- "$cur") ) ;;
        esac
        return 0
    fi

    # Level 3+: context-aware completions
    if [ "$cmd" = "config" ]; then

        # config get <key> / config set <key>: suggest config keys
        if [ "$cword" -eq 3 ] && { [ "$subcmd" = "get" ] || [ "$subcmd" = "set" ]; }; then
            local keys
            keys=$(genwal config keys 2>/dev/null)
            COMPREPLY=( $(compgen -W "$keys" -- "$cur") )
            return 0
        fi

        # config set <key> <value>: suggest valid values for the key
        if [ "$cword" -eq 4 ] && [ "$subcmd" = "set" ]; then
            local opts
            opts=$(genwal config options "${words[3]}" 2>/dev/null)
            if [ -n "$opts" ]; then
                COMPREPLY=( $(compgen -W "$opts" -- "$cur") )
            fi
            return 0
        fi

        # config get <key> — no more args after the key
        if [ "$cword" -ge 4 ] && [ "$subcmd" = "get" ]; then
            COMPREPLY=()
            return 0
        fi

        return 0
    fi

    # theme use <name> / theme edit <name>
    if [ "$cmd" = "theme" ] && [ "$cword" -eq 3 ]; then
        if [ "$subcmd" = "use" ] || [ "$subcmd" = "edit" ]; then
            COMPREPLY=( $(compgen -W "minimal stoic terminal" -- "$cur") )
            return 0
        fi
    fi

    return 0
}

complete -o nosort -F _genwal_completions genwal
