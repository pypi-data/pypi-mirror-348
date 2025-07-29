# Copyright 2024 Liu Siyao
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import logging
from pathlib import Path

from pptx2md.entry import convert
from pptx2md.log import setup_logging
from pptx2md.types import ConversionConfig

setup_logging(compat_tqdm=True)
logger = logging.getLogger(__name__)


def parse_args() -> ConversionConfig:
    arg_parser = argparse.ArgumentParser(description='Convert pptx to markdown')
    arg_parser.add_argument('pptx_path', type=Path, help='path to the pptx file to be converted')
    arg_parser.add_argument('-t', '--title', type=Path, help='path to the custom title list file')
    arg_parser.add_argument('-o', '--output', type=Path, help='path of the output file')
    arg_parser.add_argument('-i', '--image-dir', type=Path, help='where to put images extracted')
    arg_parser.add_argument('--image-width', type=int, help='maximum image with in px')
    arg_parser.add_argument('--disable-image', action="store_true", help='disable image extraction')
    arg_parser.add_argument('--disable-video', action="store_true", help='disable video extraction')
    arg_parser.add_argument('--disable-wmf',
                            action="store_true",
                            help='keep wmf formatted image untouched(avoid exceptions under linux)')
    arg_parser.add_argument('--disable-color', action="store_true", help='do not add color HTML tags')
    arg_parser.add_argument('--disable-escaping',
                            action="store_true",
                            help='do not attempt to escape special characters')
    arg_parser.add_argument('--disable-notes', action="store_true", help='do not add presenter notes')
    arg_parser.add_argument('--enable-slides', action="store_true", help='deliniate slides `\n---\n`')
    arg_parser.add_argument('--debug', action="store_true", help='enable debug mode with more detailed logging')
    arg_parser.add_argument('--try-multi-column', action="store_true", help='try to detect multi-column slides')
    arg_parser.add_argument('--wiki', action="store_true", help='generate output as wikitext(TiddlyWiki)')
    arg_parser.add_argument('--mdk', action="store_true", help='generate output as madoko markdown')
    arg_parser.add_argument('--qmd', action="store_true", help='generate output as quarto markdown presentation')
    arg_parser.add_argument('--min-block-size',
                            type=int,
                            default=15,
                            help='the minimum character number of a text block to be converted')
    arg_parser.add_argument("--page", type=int, default=None, help="only convert the specified page")
    arg_parser.add_argument(
        "--keep-similar-titles",
        action="store_true",
        help="keep similar titles (allow for repeated slide titles - One or more - Add (cont.) to the title)")

    args = arg_parser.parse_args()

    # Determine output path if not specified
    if args.output is None:
        extension = '.tid' if args.wiki else '.qmd' if args.qmd else '.md'
        args.output = Path(f'out{extension}')

    # 如果启用了调试模式，设置日志级别为 DEBUG
    if args.debug:
        import logging
        logging.getLogger().setLevel(logging.DEBUG)
        logging.getLogger("pptx2md").setLevel(logging.DEBUG)
        # 记录每个shape的详细信息
        for handler in logging.getLogger().handlers:
            handler.setLevel(logging.DEBUG)

    return ConversionConfig(
        pptx_path=args.pptx_path,
        output_path=args.output,
        image_dir=args.image_dir or args.output.parent / 'img',
        title_path=args.title,
        image_width=args.image_width,
        disable_image=args.disable_image,
        disable_video=args.disable_video,
        disable_wmf=args.disable_wmf,
        disable_color=args.disable_color,
        disable_escaping=args.disable_escaping,
        disable_notes=args.disable_notes,
        enable_slides=args.enable_slides,
        debug=args.debug,
        try_multi_column=args.try_multi_column,
        is_wiki=args.wiki,
        is_mdk=args.mdk,
        is_qmd=args.qmd,
        min_block_size=args.min_block_size,
        page=args.page,
        keep_similar_titles=args.keep_similar_titles,
    )


def main():
    config = parse_args()
    convert(config)


if __name__ == '__main__':
    main()
