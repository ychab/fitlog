const baseResourceApp = {
  delimiters: ['[[', ']]'],
  el: '#app',
  data() {
    return {
      messages: {},
      formErrors: {},
      modalMessages: {},

      loading: true,
      // filtering: false,
      paging: false,
      creating: false,
      updating: false,
      deleting: false,

      pager: {
        count: null,
        size: 20,
        delta: 2,
        previous: false,
        current: 1,
        next: 2,
        range: [],
      },

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
        this._updatePager(response.data.count)
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
          this._updatePager(response.data.count)
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
    },

    _updatePager(count) {
      this.pager.count = count
      let last = Math.round(this.pager.count / this.pager.size)

      this.pager.previous = this.pager.current > 1 ? this.pager.current - 1 : false
      this.pager.next = (this.pager.current + 1) <= last ? this.pager.current + 1 : false

      // Thanks bro!
      // @see https://gist.github.com/kottenator/9d936eb3e4e3c3e02598
      let left = this.pager.current - this.pager.delta
      let right = this.pager.current + this.pager.delta + 1
      let range = []
      let rangeWithDots = []
      let l;

      for (let i = 1; i <= last; i++) {
        if (i == 1 || i == last || i >= left && i < right) {
          range.push(i);
        }
      }

      for (let i of range) {
        if (l) {
          if (i - l === 2) {
            rangeWithDots.push(l + 1);
          } else if (i - l !== 1) {
            rangeWithDots.push('...');
          }
        }
        rangeWithDots.push(i);
        l = i;
      }

      this.pager.range = rangeWithDots;
    },

    changePage(pageNum) {
      this.paging = true
      this.pager.current = pageNum

      axios
        .get('/api/' + this.resourcePath + '/', {
          params: {
            page: pageNum,
            page_size: this.pager.size
          }
        })
        .then(response => {
          this.resources = response.data.results
          this._updatePager(response.data.count)
        })
        .finally(() => this.paging = false)
    }
  }
}
