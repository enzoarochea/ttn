"""Form field helpers (labels, hints, error slots wired with aria-describedby)."""


def field(fid, name, label, kind="text", required=True, placeholder="", autocomplete="", hint="", attrs=""):
    opt = "" if required else ' <span class="opt">(opcional)</span>'
    req = " required" if required else ""
    desc = f"{fid}-error" + (f" {fid}-hint" if hint else "")
    hint_html = f'<p class="field__hint" id="{fid}-hint">{hint}</p>' if hint else ""
    ac = f' autocomplete="{autocomplete}"' if autocomplete else ""
    ph = f' placeholder="{placeholder}"' if placeholder else ""
    if kind == "textarea":
        ctrl = f'<textarea id="{fid}" name="{name}"{req}{ph} aria-describedby="{desc}"{attrs}></textarea>'
    elif kind == "select":
        ctrl = f'<select id="{fid}" name="{name}"{req} aria-describedby="{desc}"{attrs}>{placeholder}</select>'
    else:
        ctrl = f'<input id="{fid}" name="{name}" type="{kind}"{req}{ac}{ph} aria-describedby="{desc}"{attrs}>'
    return f"""<div class="field">
            <label for="{fid}">{label}{opt}</label>
            {ctrl}
            {hint_html}
            <p class="field__error" id="{fid}-error" aria-live="polite"></p>
          </div>"""


EMAIL_MSG = ' data-msg-type-mismatch="Escribe un correo válido, por ejemplo nombre@empresa.com."'
PHONE_ATTRS = r' inputmode="tel" pattern="[+]?[0-9][0-9 .\-]{6,19}" data-msg-pattern-mismatch="Escribe un número válido, por ejemplo +502 5555 5555."'


def consent(fid, text):
    return f"""<div class="field">
            <label class="check" for="{fid}"><input id="{fid}" name="consentimiento" type="checkbox" required aria-describedby="{fid}-error" data-msg-value-missing="Necesitamos tu autorización para responder."><span>{text}</span></label>
            <p class="field__error" id="{fid}-error" aria-live="polite"></p>
          </div>"""


def honeypot(fid):
    return f'<div class="hp" aria-hidden="true"><label for="{fid}">No completar</label><input id="{fid}" name="web" type="text" tabindex="-1" autocomplete="off"></div>'
