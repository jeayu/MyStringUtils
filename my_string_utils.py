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


def split_line(text):
    return re.split(r'\n', text)


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
        indent = settings.get("csv_to_json_indent")
        for region in self.view.sel():
            if not region.empty():
                text = self.view.substr(region)
                lines = split_line(text)
                keys = re.split(separator_regex, lines[0])
                result = [dict(zip(keys, re.split(separator_regex, value)))
                          for value in lines[1:]]
                self.view.replace(edit, region, json.dumps(
                    result, ensure_ascii=False, indent=indent))


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
                    [separator.join(i.values()) for i in text_json]
                self.view.replace(edit, region, '\n'.join(result))


class FilterDuplicatedLinesCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        # filter_duplicated_lines
        for region in self.view.sel():
            if not region.empty():
                text = self.view.substr(region)
                lines = split_line(text)
                self.view.replace(edit, region, '\n'.join(
                    sorted(set(lines), key=lines.index)))


class CsvTableSqlCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        settings = sublime.load_settings("MyStringUtils.sublime-settings")
        separator_regex = settings.get("csv_separator_regex")
        for region in self.view.sel():
            if not region.empty():
                text = self.view.substr(region)
                lines = split_line(text)
                table_name = lines[0].strip()
                comments = re.split(separator_regex, lines[1])
                fields = re.split(separator_regex, lines[2])
                field_types = re.split(
                    separator_regex, lines[3])
                self.view.replace(edit, region, self.create_table_sql(
                    table_name, fields, field_types, comments))

    def create_table_sql(self, table_name, fields, field_types, comments):
        details = ',\n  '.join(["`{0}` {1} NOT NULL COMMENT '{2}'".format(
            field, field_type, comment) for field, field_type, comment in zip(fields, field_types, comments)])
        return """
CREATE TABLE `{table_name}` (
  {details},
  PRIMARY KEY (`{primary_key}`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='{table_name}';
""".format(table_name=table_name, details=details, primary_key=fields[0])
