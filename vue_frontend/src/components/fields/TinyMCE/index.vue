<template>
  <div :class="{fullscreen:fullscreen}" class="tinymce-container" :style="{width:containerWidth}">
    <textarea :id="tinymceId" class="tinymce-textarea" />
  </div>
</template>

<script>
import { defaultProps, validateProps } from '/src/utils/fields.js'
import load from './dynamicLoadScript'
import { wysiwygTypes } from '@/utils/settings'
import { config_dataset } from '@/utils/settings'

const plugins = ['advlist anchor autolink autosave code codesample colorpicker colorpicker contextmenu directionality emoticons fullscreen hr image imagetools insertdatetime link lists media nonbreaking noneditable pagebreak paste preview print save searchreplace spellchecker tabfocus table template textcolor textpattern visualblocks visualchars wordcount accordion']
const toolbar = [
  'searchreplace undo redo | bold italic underline strikethrough blockquote removeformat | alignleft aligncenter alignright outdent indent | subscript superscript code codesample',
  'hr bullist numlist link image charmap anchor pagebreak insertdatetime media table emoticons forecolor backcolor add-accordion | preview fullscreen'
]
const menubar = 'file edit insert view format table'

const tinymceCDN = `${config_dataset.static_prefix}/tinymce/tinymce.min.js`

// https://control.hydromassage.com/assets/plugins/custom/tinymce/skins/ui/oxide-dark/skin.min.css
// https://control.hydromassage.com/assets/plugins/custom/tinymce/skins/ui/oxide-dark/content.min.css
// https://github.com/cdnjs/cdnjs/tree/master/ajax/libs/tinymce/4.1.6/skins/lightgray/fonts

export default {
  name: 'wysiwyg',
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
      skin: 'lightgray',
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
  mounted() {
    validateProps(this)

    // dynamic load tinymce from cdn
    load(tinymceCDN, (err) => {
      if (err) {
        this.$message.error(err.message)
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
    console.log('destory')
    this.destroyTinymce()
  },
  methods: {
    updateFormData(initFormData) {
      const init = initFormData[this.fieldSlug]

      if (window.tinymce) {
        window.tinymce.get(this.tinymceId).setContent(init || "")
      } else {
        this.init_value = init || ""
      }
    },
    init() {
      // dynamic load tinymce from cdn
        this.initTinymce()
    },
    initTinymce() {
      const _this = this
      window.tinymce.init({
        theme: this.theme,
        skin: this.skin,
        skin_url: `${config_dataset.static_prefix}/tinymce/${this.skin}`,

        external_plugins: {
          accordion: `${config_dataset.static_prefix}/tinymce/plugins/accordion/plugin.js`
        },

        plugin_preview_width: "1200",
        plugin_preview_height: "800",

        selector: `#${this.tinymceId}`,
        language: 'en',
        height: this.height,
        body_class: 'panel-body',
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
        // it will try to keep these URLs intact
        // https://www.tiny.cloud/docs-3x/reference/configuration/Configuration3x@convert_urls/
        // https://stackoverflow.com/questions/5196205/disable-tinymce-absolute-to-relative-url-conversions
        convert_urls: false
        // 整合七牛上传
        // images_dataimg_filter(img) {
        //   setTimeout(() => {
        //     const $image = $(img);
        //     $image.removeAttr('width');
        //     $image.removeAttr('height');
        //     if ($image[0].height && $image[0].width) {
        //       $image.attr('data-wscntype', 'image');
        //       $image.attr('data-wscnh', $image[0].height);
        //       $image.attr('data-wscnw', $image[0].width);
        //       $image.addClass('wscnph');
        //     }
        //   }, 0);
        //   return img
        // },
        // images_upload_handler(blobInfo, success, failure, progress) {
        //   progress(0);
        //   const token = _this.$store.getters.token;
        //   getToken(token).then(response => {
        //     const url = response.data.qiniu_url;
        //     const formData = new FormData();
        //     formData.append('token', response.data.qiniu_token);
        //     formData.append('key', response.data.qiniu_key);
        //     formData.append('file', blobInfo.blob(), url);
        //     upload(formData).then(() => {
        //       success(url);
        //       progress(100);
        //     })
        //   }).catch(err => {
        //     failure('出现未知问题，刷新页面，或者联系程序员')
        //     console.log(err);
        //   });
        // },
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
