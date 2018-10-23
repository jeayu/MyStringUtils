# -*- coding: utf-8 -*-
import sublime
import sublime_plugin
import re
import json


def camel2underline(camel_str):
    return re.sub(r'([a-z]|\d)([A-Z])', r'\1_\2', camel_str).lower()


def underline2camel(underline_str):
    return re.sub(r'(_\w)', lambda x: x.group(
        1)[1].upper(), underline_str.lower())


def underline2words(text):
    return ' '.join(text.split('_'))


def words2underline(text):
    return '_'.join(re.split(r'\s+', text))


def camel2words(text):
    return re.sub(r'([a-z]|\d)([A-Z])', r'\1 \2', text)


def words2camel(text):
    return underline2camel(words2underline(text))


class CamelUnderlineCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        # camel_underline
        for region in self.view.sel():
            if not region.empty():
                text = self.view.substr(region)
                text = underline2camel(
                    text) if '_' in text else camel2underline(text)
                self.view.replace(edit, region, text)


class UnderlineWordsCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        # underline_words
        for region in self.view.sel():
            if not region.empty():
                text = self.view.substr(region)
                text = underline2words(
                    text) if '_' in text else words2underline(text)
                self.view.replace(edit, region, text)


class CamelWordsCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        # camel_words
        for region in self.view.sel():
            if not region.empty():
                text = self.view.substr(region).strip()
                text = words2camel(
                    text) if ' ' in text else camel2words(text)
                self.view.replace(edit, region, text)


class JsonListCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        # json_list
        for region in self.view.sel():
            if not region.empty():
                text = self.view.substr(region)
                self.view.replace(edit, region, json.dumps(
                    text.split(), ensure_ascii=False))


class CsvJsonCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        # csv_json
        settings = sublime.load_settings("MyStringUtils.sublime-settings")
        separator_regex = settings.get("csv_separator_regex")
        for region in self.view.sel():

            if not region.empty():
                text = self.view.substr(region)
                lines = re.split(r'\n', text)
                keys = re.split(separator_regex, lines[0])
                result = [dict(zip(keys, re.split(separator_regex, value)))
                          for value in lines[1:]]
                self.view.replace(edit, region, json.dumps(
                    result, ensure_ascii=False))


class JsonCsvCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        # json_csv
        settings = sublime.load_settings("MyStringUtils.sublime-settings")
        separator = settings.get("csv_separator")
        for region in self.view.sel():
            if not region.empty():
                text = self.view.substr(region)
                text_json = json.loads(text)
                result = [separator.join(text_json[0].keys())] + \
                    [separator.join(i.values()) for i in text_json[1:]]
                self.view.replace(edit, region, '\n'.join(result))
