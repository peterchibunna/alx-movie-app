
# here we pass in a variable that will be available in the context of all views
def global_processor(request):
	return {
		'center_text': True
	}
