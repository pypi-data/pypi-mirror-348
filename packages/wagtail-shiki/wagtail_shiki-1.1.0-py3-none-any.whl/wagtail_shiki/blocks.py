import wagtail

from django.forms import Media
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from wagtail.blocks import (
    BooleanBlock,
    StructBlock,
    TextBlock,
    ChoiceBlock,
    CharBlock,
    IntegerBlock,
)
from wagtail.blocks.struct_block import StructBlockAdapter
from wagtail.telepath import register

from .settings import get_language_choices


class CodeBlock(StructBlock):
    """
    A Wagtail StreamField block for code syntax highlighting using PrismJS.
    """

    def __init__(self, local_blocks=None, **kwargs):
        # Languages included in PrismJS core
        # Review: https://github.com/PrismJS/prism/blob/gh-pages/prism.js#L602
        self.INCLUDED_LANGUAGES = (
            ("ansi", "ANSI"),
            ("text", "Plain Text"),
        )

        if local_blocks is None:
            local_blocks = []
        else:
            local_blocks = local_blocks.copy()

        language_choices, language_default = self.get_language_choice_list(
            **kwargs)

        local_blocks.extend(
            [
                (
                    "language",
                    ChoiceBlock(
                        choices=language_choices,
                        help_text=_("Coding language"),
                        label=_("Language"),
                        default=language_default or self.get_initial_languge(
                            language_choices),
                        identifier="language",
                    ),
                ),
                ("show_line_numbers", BooleanBlock(label=_("Show line numbers"),
                                                   default=True, required=False, identifier="show_line_number", help_text=_("show if checked."))),
                ("start_number", IntegerBlock(label=_("Start number"),
                                              required=False, identifier="start_number", help_text=_("(Optional)."))),
                ("title", CharBlock(label=_("Title"),
                                    required=False, identifier="title", help_text=_("Filename, etc. Leave this blank, if you don't need."))),
                ("code", TextBlock(label=_("Code"), identifier="code")),
                ("highlight_words", TextBlock(label=_("Highlight Words"),
                                              required=False, identifier="highlight_words", help_text=_("Decoration definition data.(uneditable)"))),
            ]
        )

        super().__init__(local_blocks, **kwargs)

    def get_initial_languge(self, language_choices):
        initial_lang = getattr(settings, "WAGS_INITIAL_LANGUAGE", "")
        if initial_lang in [lang[0] for lang in language_choices]:
            return initial_lang
        else:
            return "text"

    def get_language_choice_list(self, **kwargs):
        # Get default languages
        specified_languages = get_language_choices()
        # If a language is passed in as part of a code block, use it.
        language = kwargs.get("language", False)

        total_language_choices = specified_languages + self.INCLUDED_LANGUAGES

        if language in [lang[0] for lang in total_language_choices]:
            for language_choice in total_language_choices:
                if language_choice[0] == language:
                    language_choices = (language_choice,)
                    language_default = language_choice[0]
        else:
            language_choices = specified_languages + self.INCLUDED_LANGUAGES
            language_default = kwargs.get("default_language")

        return language_choices, language_default

    class Meta:
        icon = "code"
        template = "wagtail_shiki/code_block.html"
        form_classname = "code-block struct-block"
        form_template = "wagtail_shiki/code_block_form.html"


class CodeBlockAdapter(StructBlockAdapter):
    js_constructor = "wagtail_shiki.blocks.CodeBlock"

    @cached_property
    def media(self):
        structblock_media = super().media
        return Media(
            js=structblock_media._js +
            ["wagtail_shiki/js/wagtail-shiki-admin.js"],
            # ["js/wagtail-shiki-admin.js"],
            css=structblock_media._css,
        )


register(CodeBlockAdapter(), CodeBlock)
