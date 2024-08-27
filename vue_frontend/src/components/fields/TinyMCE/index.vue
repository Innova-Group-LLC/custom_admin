<template>
  <div :class="{ fullscreen: fullscreen, 'tinymce-disabled': readOnly }" class="tinymce-container" :style="{width:containerWidth}">
    <textarea :id="tinymceId" class="tinymce-textarea" />
  </div>
</template>

<script>
import { toast } from "vue3-toastify"
import { defaultProps, validateProps } from '/src/utils/fields.js'
import load from './dynamicLoadScript'
import { wysiwygTypes } from '@/utils/settings'
import { config_dataset } from '@/utils/settings'
import { getSettings, getTinyMCETheme } from '/src/utils/settings'

const plugins = ['advlist anchor autolink autosave code codesample colorpicker colorpicker contextmenu directionality emoticons fullscreen hr image imagetools insertdatetime link lists media nonbreaking noneditable pagebreak paste preview print save searchreplace spellchecker tabfocus table template textcolor textpattern visualblocks visualchars wordcount accordion customLink']
const toolbar = [
  'searchreplace undo redo | bold italic underline strikethrough blockquote removeformat | alignleft aligncenter alignright outdent indent | subscript superscript code codesample',
  'hr bullist numlist link image charmap anchor pagebreak insertdatetime media table forecolor backcolor add-accordion customLink | preview fullscreen'
]
const menubar = 'file edit insert view format table'

const tinymceCDN = `${config_dataset.static_prefix}/tinymce/tinymce.min.js`

// https://control.hydromassage.com/assets/plugins/custom/tinymce/skins/ui/oxide-dark/skin.min.css
// https://control.hydromassage.com/assets/plugins/custom/tinymce/skins/ui/oxide-dark/content.min.css
// https://github.com/cdnjs/cdnjs/tree/master/ajax/libs/tinymce/4.1.6/skins/lightgray/fonts

export default {
  name: 'TinyMCE',
  props: {
    ...defaultProps,
  },
  data(props) {
    return {
      hasChange: false,
      hasInit: false,
      tinymceId: this.fieldSlug,
      fullscreen: false,
      init_value: null,
      theme: 'modern',
      height: 260,
      width: 'auto',
    }
  },
  computed: {
    containerWidth() {
      const width = this.width
      if (/^[\d]+(\.[\d]+)?$/.test(width)) { // matches `100`, `'100'`
        return `${width}px`
      }
      return width
    }
  },
  async mounted() {
    this.emitter.on("settings-changed", settings => {
      this.destroyTinymce()
      this.initTinymce()
    })

    validateProps(this)

    // dynamic load tinymce from cdn
    load(tinymceCDN, (err) => {
      if (err) {
        console.error(err.message)
        toast(err.message, {"theme": "auto", "type": "error", "position": "top-center"})
        return
      }
      this.initTinymce()
    })
  },
  activated() {
    if (window.tinymce) {
      this.initTinymce()
    }
  },
  unmounted() {
    this.emitter.off("settings-changed")
    this.destroyTinymce()
  },
  methods: {
    updateFormData(initFormData) {
      const value = initFormData[this.fieldSlug]
      this.init_value = value || ""

      if (window.tinymce) {
        if (value === window.tinymce.get(this.tinymceId).getContent()) return
        window.tinymce.get(this.tinymceId).setContent(value || "")
      }
    },
    init() {
      // dynamic load tinymce from cdn
        this.initTinymce()
    },
    initTinymce() {
      const skin = getTinyMCETheme();
      const _this = this
      window.tinymce.init({
        theme: this.theme,
        skin: skin,
        skin_url: `${config_dataset.static_prefix}/tinymce/${skin}`,

        external_plugins: {
          accordion: `${config_dataset.static_prefix}/tinymce/plugins/accordion/plugin.js`,
          customLink: `${config_dataset.static_prefix}/tinymce/plugins/customLink/plugin.js`
        },

        plugin_preview_width: "1200",
        plugin_preview_height: "800",

        readonly: this.readOnly ? 1 : false,
        selector: `#${this.tinymceId}`,
        language: 'en',
        height: this.height,
        content_style: ".panel-readonly { cursor: not-allowed; }",
        body_class: 'panel-body ' + this.readOnly ? 'panel-readonly' : '',
        object_resizing: false,
        toolbar: toolbar,
        menubar: menubar,
        plugins: plugins,
        end_container_on_empty_block: true,
        powerpaste_word_import: 'clean',
        code_dialog_height: 450,
        code_dialog_width: 1000,
        advlist_bullet_styles: 'square',
        advlist_number_styles: 'default',
        imagetools_cors_hosts: ['www.tinymce.com', 'codepen.io'],
        default_link_target: '_blank',
        link_title: false,
        nonbreaking_force_tab: true, // inserting nonbreaking space &nbsp; need Nonbreaking Space Plugin
        init_instance_callback: editor => {
          if (_this.init_value) {
            editor.setContent(_this.init_value)
          }
          _this.hasInit = true
          editor.on('NodeChange Change KeyUp SetContent', () => {
            this.hasChange = true
            this.$emit('changed', editor.getContent())
          })
        },
        setup(editor) {
          editor.on('FullscreenStateChanged', (e) => {
            _this.fullscreen = e.state
          })
        },
        convert_urls: false
      })
    },
    destroyTinymce() {
      const tinymce = window.tinymce.get(this.tinymceId)
      if (this.fullscreen) {
        tinymce.execCommand('mceFullScreen')
      }

      if (tinymce) {
        tinymce.destroy()
      }
    },
    setContent(value) {
      window.tinymce.get(this.tinymceId).setContent(value)
    },
    getContent() {
      window.tinymce.get(this.tinymceId).getContent()
    },
    imageSuccessCBK(arr) {
      arr.forEach(v => window.tinymce.get(this.tinymceId).insertContent(`<img class="wscnph" src="${v.url}" >`))
    }
  }
}
</script>
