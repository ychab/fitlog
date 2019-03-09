const baseResourceApp = {
  delimiters: ['[[', ']]'],
  el: '#app',
  data() {
    return {
      messages: {},

      loading: true,
      creating: false,
      updating: false,

      resources: [],
      newResource: null,

      resourcePath: null,
      resourceFields: null
    }
  },
  created() {
    axios.defaults.headers.common['X-CSRFToken'] = this.$cookies.get('csrftoken')

    axios.interceptors.response.use(null, (error) => {
      let messages = []

      if (error.response.status == 400) {
        for (const field in error.response.data) {
          let msgs = error.response.data[field]
          for (let msg of msgs) {
            messages.push({type: 'danger', text: field + ' : ' + msg})
          }
        }
      } else {
        messages.push({type: 'danger', text: gettext('Oups... Looks like an error occured :/')})
      }

      this.messages = messages
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
    },
    createResource(resource) {
      this.creating = true

      axios
        .post('/api/' + this.resourcePath + '/', this._collectFieldValues(resource))
        .then(response => {
          this.reset()
          this.refresh()
        })
        .finally(() => this.creating = false)
    },
    updateResource(resource) {
      this.updating = resource.id

      axios
        .patch('/api/' + this.resourcePath + '/' + resource.id + '/', this._collectFieldValues(resource))
        .finally(() => this.updating = false)
    },
    deleteResource(resource) {
      axios
        .delete('/api/' + this.resourcePath + '/' + resource.id + '/')
        .then(response => {
          $('#modal-delete-' + resource.id).modal('hide')
          this.refresh()
        })
    }
  }
}
