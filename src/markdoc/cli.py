# -*- coding: utf-8 -*-

import os

import argparse


parser = argparse.ArgumentParser(**{
    'prog': 'markdoc',
    'description': 'A Markdown-based documentation build tool',
    'version': '1.0'
})

parser.add_argument('--config', '-c', default=os.getcwd())

subparsers = parser.add_subparsers(dest='command')


if __name__ == '__main__':
    args = parser.parse_args()
    # TODO: implement task runner.
