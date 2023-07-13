from django import template
from django.utils.http import urlencode
import re
register = template.Library()


def str_to_boolean(s):
	if s.lower() in ['true', '1', 't', 'y', 'yes']:
		return True
	elif s.lower() in ['false', '0', 'f', 'n', 'no']:
		return False
	return str(s)


@register.simple_tag(takes_context=True)
def query_params(context, **kwargs):
	query = context['request'].GET.dict()
	query.update(kwargs)
	return urlencode(query)


@register.filter(name='str_to_dict')
def str_to_dict(value, arg):
	response = {}
	if arg == ' ':
		PATTERN = re.compile('''((?:[^({})"']|"[^"]*"|'[^']*')+)'''.format(arg))
		for i in PATTERN.split(value)[1::2]:
			if i.strip() != '':
				k, v = i.split("=")
				response[k] = str_to_boolean(v.replace('"', ''))
	else:
		for i in value.strip().split(arg):
			if i.strip() != '':
				k, v = i.split("=")
				response[k] = str_to_boolean(v.replace('"', ''))
	return response
