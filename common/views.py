class CommonMixin:
    title = None
    def get_context_data(self):
        context = super(CommonMixin, self).get_context_data()
        context['title'] = self.title
        return context