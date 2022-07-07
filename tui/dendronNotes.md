# Importing notes into dendron

## current bash script:

```batch
vaultName: vault\n\
indexName: index.md" \
> ${notesRoot}configTest.yml

echo "importing to dendron..."
dendron importPod --podId dendron.markdown \
--wsRoot '/Users/tculpepp/Documents/repos/dendron' \
--config src=~/Downloads/CSC316/toImport,vaultName=vault,indexName=index.md
--config src=${importRoot},vaultName=vault,indexName=index.md
```

# dendron wiki

- to configure the import pod: run > configurepod in vsCode

```
dendron importPod --podID dendron.markdown --wsRoot .
```

## configuration

- **src**
    - description: where to import from
    - type: "string" as const
    - required: true
- **vaultName**
    - description: "name of vault to import into"
    - type: :string" as const
    - required: true
- **concatenate**
    - description: whether to concat everything into one note
    - type: boolean
    - required: false
    - when importing you can either import everything from source and multiple files or concat it all together as one file
- **frontmatter**
    - description: frontmatter to add to each note
    - type: object
    - you can add custom frontmatter to notes as you import them. This is useful for example, when you want to set custom publishing options for imported notes
- **fnameAsId**
    - description: use filename as the id
    - type: boolean
    - by default, random uuids are generated as the ID for each imnported note. This makes the ID equivalent to that of the filename
- **destName**
    - description: "if concatenate option is set, this is the name of the destination path
    - type: "string" as const
- **noAddUUID**
    - default: false
    - description: if set, don't append random uuid to asset files
- **indexName**
    - default: none
    - if set, match the given indexName and combine it with the imported directory. for example, some services like gitbook will use index.md as an index for the cirectory
    - matching is case insensitive and "doesn't require the extension"
- **importFrontmatter
    - default: true
    - type: boolean
    - if set, imports the note metadata as well. if there is a conflict, dendron appends "_imported"


## import pod options

```
--version           show version number [boolean]
--help              show help [boolean]
--wsRoot            location of workspace
--vault             name of vault
--quiet             don't pring output to stdout
--enginePort        if set, connect to running engine. If not set, create new instance of dendron engine
--attach            use existing engine instead of spawning a new one
--useLocalEngine    If set, use in memory engine instead of connecting to a server [boolean]
--podId             ID of pod to use
--showConfig        show pod configuration
--genConfig         show pod configuration
--podPkg            if specifying a custom pod, name of pkg
--config            pass in config instead of reading from file. format is comma delimited {key}={value} pairs
--podSource         podSource[choices: "custom", "builtin"] [default: "builtin"]
```
## Notes
- podId should be dendron.markdown

## file structure for import

### Before Import
```
.
└── projects
    ├── p1
    |   ├── one.md
    |   ├── two.md
    |   └── one.pdf
    └── p2
        ├── three.md
        ├── four.md
        └── three.gif
```
### After Import
```
.
└── vault
    ├── assets
    |   ├── one--{uuid}.pdf
    |   └── three--{uuid}.gif
    ├── projects.p1.md
    ├── projects.p1.one.md
    ├── projects.p1.two.md
    ├── projects.p2.md
    ├── projects.p2.three.md
    └── projects.p2.four.md
```

