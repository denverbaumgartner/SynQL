#!/usr/bin/env sh

python_command() {
    poetry run python
}

shell_command() {
    poetry shell
}

test_command() {
    poetry run pytest tests
}

specify_test_command() {
    poetry run pytest -s tests/$1
}

# accept_command() {
#     poetry run pytest tests/acceptance
# }

# lint_command() {
#     poetry run pyright .
# }

# format_command() {
#     poetry run isort .
#     poetry run black .
# }

# all_command() {
#     lint_command
#     format_command
#     test_command
# }

# mkdocs_command() {
#     poetry run mkdocs serve
# }

install_command() {
    poetry install --without dev
}

dev_command() {
    poetry install --with docs,dev
}

show_help() {
    echo "Usage: ./nli [option]"
    echo "Options:"
    echo "  accept                 Run acceptance tests"
    echo "  python                 Run Python"
    echo "  shell                  Run a shell in the virtual environment"
    echo "  test                   Run pytest"
    echo "  specify                Run specific pytest file"
    echo "  lint                   Run pyright"
    echo "  format                 Run isort and black"
    echo "  all                    Run lint, format, and test"
    echo "  mkdocs                 Serve mkdocs"
    echo "  install                Install without dev dependencies"
    echo "  dev                    Install with docs dependencies"
}

if [ -z "$1" ]; then
    show_help
else
    case "$1" in
        "accept") accept_command ;;
        "python") python_command ;;
        "shell") shell_command ;;
        "test") test_command ;;
        "specify") specify_test_command $2 ;;
        # "lint") lint_command ;;
        # "format") format_command ;;
        # "all") all_command ;;
        # "mkdocs") mkdocs_command ;;
        "install") install_command ;;
        "dev") dev_command ;;
        *) show_help ;;
    esac
fi
