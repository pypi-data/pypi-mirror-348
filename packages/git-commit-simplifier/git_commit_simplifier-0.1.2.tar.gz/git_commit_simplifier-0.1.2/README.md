# Git Commit Simplifier

A command-line tool that simplifies Git commit message creation by analyzing your changes and suggesting meaningful commit messages.

## Features

- Automatically analyzes staged changes in your Git repository
- Categorizes files based on their type and purpose
- Detects the nature of changes (feature, fix, refactor, etc.)
- Generates structured, informative commit messages
- Supports multiple commit message styles (detailed, conventional, simple)
- Optional emoji support in commit messages
- Interactive mode for selecting files to stage
- Allows editing the suggested message before committing
- Option to push changes after committing
- Configurable via command-line options or configuration file

## Installation

```pip install git-commit-simplifier```
# or 
```pip3 install git-commit-simplifier```

## Usage

Navigate to your Git repository and run:

```git-commit-simplifier```

### Options

```
--path TEXT                     Path to the Git repository (default: current directory)
--preview / --no-preview        Preview changes before committing (default: enabled)
--edit / --no-edit              Edit the commit message before committing (default: enabled)
--push / --no-push              Push changes after committing (default: disabled)
--style [detailed|conventional|simple]
                                Commit message style
--emoji / --no-emoji            Use emoji in commit messages
--interactive / --no-interactive
                                Use interactive mode for staging
--version                       Show the version and exit
--help                          Show this message and exit
```

### Commands

```config```  Configure git-commit-simplifier settings

## Configuration

You can configure git-commit-simplifier using the `config` command:

```git-commit-simplifier config --style conventional --emoji --auto-push```

Configuration is stored in `~/.git-commit-simplifier.json` or `.git-commit-simplifier.json` in your repository.

## Commit Message Styles

### Detailed (Default)

```Add user authentication```

## python
```- Add src/auth.py (new file, authentication implementation)```
```- Update src/app.py (dependency changes, function definition changes)```

## configuration
```- Add config/auth.yaml (new file)```

### Conventional

Follows the Conventional Commits specification:

```feat(auth): implement user authentication```

## python
```- Add src/auth.py (new file, authentication implementation)```
```- Update src/app.py (dependency changes, function definition changes)```

## configuration
```- Add config/auth.yaml (new file)```

### Simple

```Add user authentication```

## License

MIT License