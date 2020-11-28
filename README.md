# roam2agora

`roam2agora` is a privacy-respecting CLI utility to export _part_ of your roam graph to markdown. You can use the files as is in the agora at https://anagora.org/ (ping [@flancian](https://twitter.com/flancian) to have your garden added to the public agora) or use them to build your own agora.


## tl;dr
- Add `#public` or `#public_page` to blocks in your roam graph, and export your graph as JSON
- Download and install roam2agora from the [releases page](https://github.com/nikvdp/roam2agora/releases).
- Run `roam2agora -i <your-roam-export>.json -o ~/<your-agora-folder>` 
- `~/<your-agora-folder>` now contains markdown versions of just the public parts of your graph, ready for upload to [the agora](https://anagora.org/) or use in a digital garden.

## Features

Privacy controls!
`roam2agora` let's you specify which blocks or pages you'd like to share, via a set of special tags:

- Tagging a block with `#public` will cause that block (and any subblocks) to be exported to the agora
- Tagging a block with `#private` will *prevent* a block from being exported to the agora. You can mix and match this with `#public` if you'd like to export a top-level block, but not some of it's descendants. `#private` always takes priority over public.
- Tagging a block with `#public_page` anywhere on a page will cause the entire page to be exported to the agora. You can still use `#private` tags on the page if there are parts of the page that you don't want to include in the export.
- Tagging a block with `#private_page` will prevent a page from being exported. Be careful, `#private_page` takes precedence over `#public` and `#public_page`, so if you include a `#private_page` block on a page that also has a `#public` block the entire page will be excluded from the export.

## Caveats

> ⚠️ `roam2agora` is early stage software! Use at your own risk and make sure to manually check that nothing that you didn't want shared gets included in the export.

## Installation

The easiest way to get up and running is to download roam2agora for your platform from the [releases page](https://github.com/nikvdp/roam2agora/releases). 

Once downloaded, on mac and linux you'll have to first run `chmod +x ./roam2agora` to make it executable, and then copy it to a local on your `PATH` (`/usr/bin/local` is a common choice if you're not sure). On Windows no `chmod +x` step is required.



## Usage

### Prepare a JSON roam export

First, you need to export the roam graph that contains the content you'd like to publish from the agora. 

- To do this (as of Nov 2020), click the "..." icon at the upper right of Roam and choose `Export All.`

    ![README%20md%20998d8b3f584a46e5a0560a0a59d1c74b/Untitled.png](.github/roam-export.png)

- Make sure to choose `JSON` for the export format:

    ![README%20md%20998d8b3f584a46e5a0560a0a59d1c74b/Untitled%201.png](.github/roam-export-json.png)

- Unzip the zip file, and take note of the path to the `.json` file that comes out.

### Install and run roam2agora

Once you've got your roam export prepared, install `roam2agora` via `pip`:

```bash
pip install git+ssh://git@github.com/nikvdp/roam2agora.git#egg=roam2agora
```

If all went well you can now see the usage instructions via `roam2agora --help`:

```bash
Usage: roam2agora [OPTIONS]

Options:
  -i, --roam-export-file FILE
  -o, --output-folder DIRECTORY
  --follow-refs / -d, --dont-follow-refs
  -p, --default-public / --default-closed
  -h, --help                      Show this message and exit.
```

To run it, use the `-i` option to specify the source import file you saved earlier, and the `-o` option to specify an agora folder to save the resulting markdown files too. For example, if you unzippped the roam json to your home folder's `Downloads` directory, you'd run a command like the below (replacing `<graph-name>` with your graph's name of course).

```bash
roam2agora -i ~/Downloads/<graph-name>.json -o ~/agora
```

You're done! Just make sure to **check all your files to make sure that nothing you want to stay private was accidentally included** in the export!

### Advanced use cases

There are a few options available for more specific use cases:

- `--dont-follow-refs` 

  This flag tells `roam2agora` to avoid block transclusion. 

  In other words, if you're roam node looks like 'This is some roam text that references block ((g4Q8llgTD))', and you have `--follow-refs` enabled (the default) the outputted markdown will include the text of block `((g4Q8llgTD))` unless block `g4Q8llgTD` has been tagged with `#private`.

  If you use `--dont-follow-refs`, then the markdown export will just show 'This is some roam text that references block ((g4Q8llgTD))'

- `--default-public`

  If you use this flag then all files in your graph will be considered public by default.

  In other words, unless you use the `#private_page` tag on a page, it will be included in the outputted markdown files 

### Add your files to the agora

All that's left is to get your new markdown folder into the public agora! To do this, get in touch with [@flancian](https://twitter.com/flancian) on twitter or take a look at the [agora's github repo](https://github.com/flancian/agora).
