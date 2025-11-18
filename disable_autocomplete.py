"""
Utility to disable password autocomplete on non-password text inputs.

Browser password managers often incorrectly flag regular text inputs
as "new password" fields. This module injects JavaScript to add proper
autocomplete attributes to prevent this behavior.
"""

import streamlit as st
import streamlit.components.v1 as components

def disable_password_autocomplete():
    """
    Inject JavaScript to prevent browsers from treating regular text inputs
    as password fields.

    This adds autocomplete="off" to all text inputs that are NOT password fields,
    preventing password managers from incorrectly flagging them.

    Should be called once per page, typically near the top after page config.
    """
    components.html(
        """
        <script>
        // Wait for Streamlit to render
        const disablePasswordAutocomplete = () => {
            // Find all text input elements
            const inputs = document.querySelectorAll('input[type="text"], input[type="number"]');

            inputs.forEach(input => {
                // Only modify if it doesn't already have autocomplete set
                if (!input.hasAttribute('autocomplete')) {
                    input.setAttribute('autocomplete', 'off');
                }
            });

            // Also handle inputs that might be added dynamically
            const observer = new MutationObserver((mutations) => {
                mutations.forEach((mutation) => {
                    mutation.addedNodes.forEach((node) => {
                        if (node.nodeType === 1) { // Element node
                            const newInputs = node.querySelectorAll('input[type="text"], input[type="number"]');
                            newInputs.forEach(input => {
                                if (!input.hasAttribute('autocomplete')) {
                                    input.setAttribute('autocomplete', 'off');
                                }
                            });
                        }
                    });
                });
            });

            // Start observing the document for changes
            const targetNode = document.body;
            const config = { childList: true, subtree: true };
            observer.observe(targetNode, config);
        };

        // Run after a short delay to ensure Streamlit has rendered
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => {
                setTimeout(disablePasswordAutocomplete, 100);
            });
        } else {
            setTimeout(disablePasswordAutocomplete, 100);
        }
        </script>
        """,
        height=0,
        width=0,
    )

def set_proper_autocomplete_attributes():
    """
    More comprehensive solution that sets appropriate autocomplete values
    for different input types.

    - Password fields: keep their autocomplete="new-password" or "current-password"
    - Email/URL fields: use autocomplete="off"
    - Path/config fields: use autocomplete="off"
    - Regular text: use autocomplete="off"
    """
    components.html(
        """
        <script>
        const setAutocompleteAttributes = () => {
            // Handle text inputs
            const textInputs = document.querySelectorAll('input[type="text"]');
            textInputs.forEach(input => {
                // Check if it's a password field based on parent context
                const isPasswordField = input.getAttribute('type') === 'password';
                if (isPasswordField) {
                    return; // Skip password fields
                }

                // Force set autocomplete to off for all non-password text inputs
                input.setAttribute('autocomplete', 'off');
                input.setAttribute('data-lpignore', 'true'); // LastPass ignore
                input.setAttribute('data-form-type', 'other'); // Chrome ignore
            });

            // Handle number inputs (definitely not passwords!)
            const numberInputs = document.querySelectorAll('input[type="number"]');
            numberInputs.forEach(input => {
                input.setAttribute('autocomplete', 'off');
                input.setAttribute('data-lpignore', 'true');
                input.setAttribute('data-form-type', 'other');
            });

            // Monitor for new inputs added dynamically
            const observer = new MutationObserver((mutations) => {
                mutations.forEach((mutation) => {
                    mutation.addedNodes.forEach((node) => {
                        if (node.nodeType === 1) {
                            const inputs = node.querySelectorAll('input[type="text"], input[type="number"]');
                            inputs.forEach(input => {
                                const isPasswordField = input.getAttribute('type') === 'password';
                                if (!isPasswordField) {
                                    input.setAttribute('autocomplete', 'off');
                                    input.setAttribute('data-lpignore', 'true');
                                    input.setAttribute('data-form-type', 'other');
                                }
                            });
                        }
                    });
                });
            });

            observer.observe(document.body, { childList: true, subtree: true });
        };

        // Execute multiple times to catch all Streamlit rendering phases
        const runMultipleTimes = () => {
            setAutocompleteAttributes();
            setTimeout(setAutocompleteAttributes, 100);
            setTimeout(setAutocompleteAttributes, 300);
            setTimeout(setAutocompleteAttributes, 500);
            setTimeout(setAutocompleteAttributes, 1000);
        };

        // Execute on page load
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', runMultipleTimes);
        } else {
            runMultipleTimes();
        }

        // Also run on Streamlit reruns (when page content changes)
        window.addEventListener('load', runMultipleTimes);
        </script>
        """,
        height=0,
        width=0,
    )
