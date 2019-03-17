const baseResourceApp = {
  delimiters: ['[[', ']]'],
  el: '#app',
  data() {
    return {
      messages: {},
      formErrors: {},
      modalMessages: {},

      loading: true,
      creating: false,
      updating: false,
      deleting: false,

      resources: [],
      newResource: null,

      resourcePath: null,
      resourceFields: null
    }
  },
  created() {
    axios.defaults.headers.common['X-CSRFToken'] = this.$cookies.get('csrftoken')
    axios.interceptors.response.use(null, (error) => {
      this.messages = this._getMessageErrors(error)
      this.formErrors = this._getFormErrors(error)
      console.log(error)
      return Promise.reject(error)
    })
  },
  mounted() {
    this.reset()

    axios
      .get('/api/' + this.resourcePath + '/')
      .then(response => {
        this.resources = response.data.results
      })
      .finally(() => this.loading = false)
  },
  methods: {
    _getMessageErrors(error) {
      let messages = []

      if (error.response.status == 400) {
        for (const field in error.response.data) {
          if (field === 'non_field_errors') {
            for (let msg of error.response.data[field]) {
              messages.push({type: 'danger', text: field + ' : ' + msg})
            }
          }
        }
      } else {
        messages.push({type: 'danger', text: gettext('Oups... Looks like an error occured :/')})
      }

      return messages
    },
    _getFormErrors(error) {
      let errors = []

      if (error.response.status == 400) {
        for (const field in error.response.data) {
          if (field !== 'non_field_errors') {
            errors[field] = error.response.data[field]
          }
        }
      }

      return errors
    },
    hasFormFieldErrors(selector) {
      let formErrors = { ... this.formErrors}
      let parts = selector.split('.')
      for (let part of parts) {
        if (part in formErrors) {
          formErrors = formErrors[part]
        } else {
          return false
        }
      }
      return true
    },
    _collectFieldValues(resource) {
      let postData = {}
      for (const fieldName in this.resourceFields) {
        postData[fieldName] = resource[fieldName]
      }
      return postData
    },
    reset() {
      let newResource = {}
      for (const fieldName in this.resourceFields) {
        let field = this.resourceFields[fieldName]
        newResource[fieldName] = field.default
      }
      this.newResource = newResource
    },
    refresh() {
      axios
        .get('/api/' + this.resourcePath + '/')
        .then(response => {
          this.resources = response.data.results
        })
        .finally(() => this.loading = false)
    },
    closeModal() {
      this.messages = {}
      this.formErrors = {}
      this.reset()
      this.refresh()
    },
    createResource(resource) {
      this.creating = true

      axios
        .post('/api/' + this.resourcePath + '/', this._collectFieldValues(resource))
        .then(response => {
          this.reset()
          this.formErrors = {}
          this.refresh()
        })
        .finally(() => this.creating = false)
    },
    updateResource(resource) {
      this.updating = resource.id

      axios
        .patch('/api/' + this.resourcePath + '/' + resource.id + '/', this._collectFieldValues(resource))
        .then(response => {
          this.formErrors = {}
        })
        .finally(() => this.updating = false)
    },
    deleteResource(resource) {
      this.deleting = true

      axios
        .delete('/api/' + this.resourcePath + '/' + resource.id + '/')
        .then(response => {
          $('#modal-delete-' + resource.id).modal('hide')
          this.refresh()
        })
        .finally(() => this.deleting = false)
    }
  }
}
