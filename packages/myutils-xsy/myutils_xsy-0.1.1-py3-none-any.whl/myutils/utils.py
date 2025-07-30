from jinja2 import Environment, BaseLoader, TemplateSyntaxError
from markupsafe import escape
from collections import OrderedDict
import re

def render_html(template_text, data, default_values, source="user"):
    def highlight(value, key):
        if isinstance(value, list):
            rows = []
            for row in value:
                cells = []
                for fld, cell in row.items():
                    cell_val = str(cell).strip() if cell else default_values.get(key, {}).get("default", "")
                    color = "blue" if str(cell).strip() else "red"
                    escaped = escape(cell_val).replace('\n', '<br>\n')
                    cells.append(f'<span style="color:{color}">{escaped}</span>')
                rows.append(' | '.join(cells))
            return '<br>\n'.join(rows)
        elif isinstance(value, bool):
            # color = "blue"  # Checkboxes are always user-controlled
            # disp_text = "是" if value else "否"
            # return f'<span style="color:{color}">{disp_text}</span>'
            return ''  # 直接跳过复选框变量渲染
        else:
            # Convert value to string for comparison
            orig_text = str(value).strip() if value is not None else ''
            default_val = default_values.get(key, {}).get("default", "")
            # Check if the value matches the default (or is empty and default applies)
            is_default = orig_text == '' or orig_text == str(default_val)
            disp_text = orig_text if orig_text else default_val
            disp_escaped = escape(disp_text).replace('\n', '<br>\n')
            color = "red" if is_default else "blue"
            return f'<span style="color:{color}">{disp_escaped}</span>'

    # Create Jinja2 environment
    # env = Environment()
    env = Environment(
            trim_blocks=True,
            lstrip_blocks=True
        )
    env.filters['highlight'] = highlight

    # Prepare data with proper types
    context = {}
    for k, v in data.items():
        if default_values.get(k, {}).get("type") == "checkbox":
            context[k] = bool(v)
        else:
            context[k] = v

    try:
        # Modify the template to apply highlight filter to all variables
        modified_template = template_text
        # for var in default_values.keys():
        #     modified_template = re.sub(
        #         rf"{{{{\s*{var}\s*(?!\|\s*\w+)\s*}}}}",
        #         f"{{{{ {var} | highlight('{var}') }}}}",
        #         modified_template
        #     )
        for var in default_values.keys():
            modified_template = re.sub(
                rf"{{{{\s*{var}[^}}]*}}}}",  # 匹配 {{ var ... }}，中间可以有任意过滤器
                f"{{{{ {var} | highlight('{var}') }}}}",
                modified_template
            )
        #     print("🛠️ 自动加 highlight 后的模板：")
        # print(modified_template)
        
        # Render the modified template
        tmpl = env.from_string(modified_template)
        rendered = tmpl.render(**context)
        
        # Convert newlines to HTML breaks
        rendered = rendered.replace('\n', '<br>\n')
        return rendered
    except TemplateSyntaxError as e:
        return f"模板语法错误：{str(e)}"
    except Exception as e:
        return f"渲染错误：{str(e)}"
    
def extract_variables_with_defaults(template_text):
    template_text = re.sub(r"{#\s*filename:.*?#}", "", template_text, flags=re.DOTALL)
    combined_pattern = re.compile(
        r"{#\s*type:(?P<type>\w+)(?:\s+name:(?P<list_name>\w+)\s+fields:(?P<list_fields>[\w,]+))?\s*#}"
        r"|{{\s*(?P<var>\w+)(?:\s*\|\s*default\((?P<q>['\"])?(?P<def>.*?)(?P=q)?\))?\s*}}"
    )

    seen = OrderedDict()
    pending_type = None

    for m in re.finditer(combined_pattern, template_text):
        if m.group('type'):
            if m.group('type').lower() == 'list' and m.group('list_name'):
                name = m.group('list_name')
                fields = m.group('list_fields').split(',')
                seen[name] = {"type": "list", "fields": fields, "default": []}
            else:
                pending_type = m.group('type').lower()
        elif m.group('var'):
            var = m.group('var')
            default = m.group('def')
            input_type = pending_type if pending_type else 'singleline'
            if input_type == 'checkbox':
                default_val = str(default).lower() if default else 'false'
                default = default_val in ("true", "1", "yes")
            elif not default:
                default = f"请输入：{var}"
            seen[var] = {"type": input_type, "default": default}
            pending_type = None
    return seen