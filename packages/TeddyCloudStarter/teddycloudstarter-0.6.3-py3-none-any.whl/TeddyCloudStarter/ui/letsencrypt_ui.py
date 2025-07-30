#!/usr/bin/env python3
"""
Let's Encrypt UI functionality for TeddyCloudStarter.
"""
import questionary

from ..wizard.ui_helpers import console, custom_style
from ..utilities.logger import logger


def display_letsencrypt_not_available_warning(domain, translator):
    """
    Display warning that Let's Encrypt isn't available due to unresolvable domain.

    Args:
        domain: The domain that isn't resolvable
        translator: The translator instance for localization
    """
    logger.debug(f"Displaying Let's Encrypt not available warning for domain: {domain}")
    console.print(f"\n[bold yellow]{translator.get('Warning')}:[/]")
    console.print(
        f"[yellow]{translator.get('The domain')} '{domain}' {translator.get('does not appear to be publicly resolvable')}.[/]"
    )
    console.print(
        f"[yellow]{translator.get('Let\'s Encrypt requires a publicly accessible domain to verify ownership')}.[/]"
    )
    console.print(
        f"[yellow]{translator.get('You can use self-signed certificates or provide your own certificates instead')}.[/]\n"
    )
    logger.info("Displayed Let's Encrypt not available warning.")


def display_letsencrypt_requirements(translator):
    """
    Display Let's Encrypt requirements info.

    Args:
        translator: The translator instance for localization
    """
    logger.debug("Displaying Let's Encrypt requirements info.")
    console.print(f"\n[bold cyan]{translator.get('Let\'s Encrypt Requirements')}:[/]")
    console.print(
        f"[cyan]- {translator.get('Your server must be publicly accessible on ports 80 and 443')}"
    )
    console.print(
        f"[cyan]- {translator.get('Your domain must point to this server\'s IP')}"
    )
    console.print(
        f"[cyan]- {translator.get('Let\'s Encrypt has rate limits, so testing might use up your attempts')}\n"
    )
    logger.info("Displayed Let's Encrypt requirements info.")


def confirm_letsencrypt_requirements(translator):
    """
    Ask user to confirm that they understand Let's Encrypt requirements.

    Args:
        translator: The translator instance for localization

    Returns:
        bool: True if confirmed, False otherwise
    """
    logger.debug("Prompting user to confirm Let's Encrypt requirements.")
    result = questionary.confirm(
        translator.get("Do you confirm that your server meets these requirements?"),
        default=True,
        style=custom_style,
    ).ask()
    logger.info(f"User confirmed Let's Encrypt requirements: {result}")
    return result


def confirm_test_certificate(translator):
    """
    Ask user if they want to test if domain is set up correctly for Let's Encrypt.

    Args:
        translator: The translator instance for localization

    Returns:
        bool: True if user wants to test, False otherwise
    """
    logger.debug("Prompting user to test if domain is set up for Let's Encrypt.")
    result = questionary.confirm(
        translator.get(
            "Would you like to test if your domain is correctly set up for Let's Encrypt?"
        ),
        default=True,
        style=custom_style,
    ).ask()
    logger.info(f"User chose to test domain for Let's Encrypt: {result}")
    return result


def display_domain_not_resolvable_warning(domain, translator):
    """
    Display warning that domain is not publicly resolvable.

    Args:
        domain: The domain that isn't resolvable
        translator: The translator instance for localization
    """
    logger.debug(f"Displaying domain not resolvable warning for domain: {domain}")
    console.print(f"\n[bold yellow]{translator.get('Warning')}:[/]")
    console.print(
        f"[yellow]{translator.get('The domain')} '{domain}' {translator.get('does not appear to be publicly resolvable')}.[/]"
    )
    console.print(
        f"[yellow]{translator.get('This may cause issues if your site needs to be publicly accessible')}.[/]\n"
    )
    logger.info("Displayed domain not resolvable warning.")


def confirm_switch_to_self_signed(translator):
    """
    Ask user if they want to switch to self-signed certificates.

    Args:
        translator: The translator instance for localization

    Returns:
        bool: True if confirmed, False otherwise
    """
    logger.debug("Prompting user to switch to self-signed certificates.")
    result = questionary.confirm(
        translator.get("Would you like to switch to self-signed certificates instead?"),
        default=True,
        style=custom_style,
    ).ask()
    logger.info(f"User chose to switch to self-signed certificates: {result}")
    return result
