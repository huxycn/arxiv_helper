import sys
import fire

from pathlib import Path
from loguru import logger

from .core.arxiv_api import ArxivApi
from .core.pattern_recognizer import PatternRecognizer
from .core.pdf_downloader import PdfDownloader


def get_pdf_name(arxiv_info):
    _id = arxiv_info['id']
    title = arxiv_info['title'].replace(' ', '_')
    author = arxiv_info['author'][0].replace(' ', '_') + '_et_al'

    pdf_name = f'{_id}_{title}_{author}.pdf'
    return pdf_name


def get_paper_info(arxiv_info):
    title = arxiv_info['title']
    author = arxiv_info['author'][0] + ' et al'
    year = arxiv_info['published'].split('-')[0]

    paper_info = f'**{title}**. {author}. {year}.'
    return paper_info


def download_from_url(arxiv_url, output_pdf_dir='.'):
    arxiv_api = ArxivApi()
    pdf_downloader = PdfDownloader()

    arxiv_id = arxiv_url.split('/')[-1]

    arxiv_info = arxiv_api.fetch_arxiv_info(arxiv_id)

    pdf_link = arxiv_info['pdf']

    pdf_path = Path(output_pdf_dir) / get_pdf_name(arxiv_info)

    pdf_downloader.download(pdf_link, pdf_path)


def get_md_files(md_file_or_dir):
    if Path(md_file_or_dir).is_dir():
        md_files = list(Path(md_file_or_dir).rglob('*.md'))
    elif Path(md_file_or_dir).is_file() and Path(md_file_or_dir).suffix == '.md':
        md_files = [Path(md_file_or_dir)]
    else:
        md_files = []
    return md_files


def download_from_mds(md_file_or_dir, output_pdf_dir='.'):
    arxiv_api = ArxivApi()
    pattern_recognizer = PatternRecognizer(r'{{https://arxiv.org/abs/\d{4}.\d{5}}}')
    pdf_downloader = PdfDownloader()

    md_files = get_md_files(md_file_or_dir)
    md_files_msg = "\n".join([str(md_file) for md_file in md_files])
    logger.info(f'md-loop ==> {len(md_files)} md files found: \n{md_files_msg}')
    for md_idx, md_file in enumerate(md_files):
        logger.info(f'md-loop ==> {md_idx}: {md_file}')
        with open(md_file, 'r') as f:
            content = f.read()

        replace_dict = {}
        arxiv_urls = pattern_recognizer.findall(content)
        arxiv_urls_msg = "\n".join([str(arxiv_url) for arxiv_url in arxiv_urls])
        logger.info(f'url-loop ==> {len(arxiv_urls)} arxiv urls found: \n{arxiv_urls_msg}')
        for url_idx, arxiv_url in enumerate(arxiv_urls):
            try:
                logger.info(f'url-loop ==> {url_idx}: {arxiv_url}')
                arxiv_url_with_braces = arxiv_url
                arxiv_url = arxiv_url[2:-2]
                arxiv_id = arxiv_url.split('/')[-1]
                arxiv_info = arxiv_api.fetch_arxiv_info(arxiv_id)
                pdf_link = arxiv_info['pdf']
                pdf_path = Path(output_pdf_dir) / get_pdf_name(arxiv_info)
                pdf_path.parent.mkdir(parents=True, exist_ok=True)

                pdf_downloader.download(pdf_link, pdf_path)

                replace_dict[arxiv_url_with_braces] = f'{arxiv_url}: {get_paper_info(arxiv_info)}'
            except Exception as e:
                logger.warning(f'url-loop ==> {url_idx}: {arxiv_url} failed: {e}')
        
        replaced_content = pattern_recognizer.multiple_replace(content, **replace_dict)
        with open(md_file, 'w') as f:
            f.write(replaced_content)
        logger.info(f'md-loop ==> {md_idx}: {md_file} updated')


def main():
    logger.remove()
    logger.add(
        sys.stdout,
        level='INFO',
    )
    fire.Fire({
        'url': download_from_url,
        'md': download_from_mds,
    })
