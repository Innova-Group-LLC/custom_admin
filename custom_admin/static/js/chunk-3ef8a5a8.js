(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-3ef8a5a8"],{"0377":function(e,t,i){"use strict";i.r(t);var l=function(){var e=this,t=e.$createElement,i=e._self._c||t;return i("el-form",{ref:"form",staticClass:"data-form",attrs:{"label-position":"left","label-width":"200px",size:"mini",model:e.formData}},[i("el-tabs",{class:e.meta.field_groups?"":"hide-header",model:{value:e.activeTab,callback:function(t){e.activeTab=t},expression:"activeTab"}},e._l(e.getGroups(),(function(t,l){return i("el-tab-pane",{key:t.title,attrs:{label:t.title}},[e._l(e.errors["non_field_errors"],(function(t){return e.errors?[i("el-alert",{staticClass:"form-error",attrs:{title:t,type:"error"}})]:e._e()})),e._l(e.meta.serializer,(function(t,a){return[e.canBeDisplayed(t,a,l)&&!e.isTranslation(a)?[-1===Object.keys(e.getTranslations()).indexOf(a)?[i("fieldelement",{ref:"field_"+a,refInFor:!0,attrs:{label:t.label,field_slug:a,field:t,"form-info":e.formInfo,"api-info":e.apiInfo,settings:e.settings,"init-form-data":e.formData},on:{changed:function(t){return e._updateValue(t,a)}}})]:[i("el-form-item",{class:{"is-required":t.required},attrs:{label:t.label,prop:a,"label-width":"230px"}},[i("el-tabs",{staticClass:"translation-tabs",attrs:{type:"border-card"}},[e._l(e.getTranslations()[a],(function(t){return[i("el-tab-pane",{key:t.lang_slug,attrs:{label:t.lang_translation,lazy:""},model:{value:e.translationsTabs[a],callback:function(t){e.$set(e.translationsTabs,a,t)},expression:"translationsTabs[field_slug]"}},[e.meta.serializer[t.slug]?i("fieldelement",{ref:"field_"+t.slug,refInFor:!0,attrs:{"label-width":"0px",placeholder:e.meta.serializer[t.slug].label,field_slug:t.slug,field:e.meta.serializer[t.slug],"form-info":e.formInfo,"api-info":e.apiInfo,settings:e.settings,"init-form-data":e.formData},on:{changed:function(i){return e._updateValue(i,t.slug)}}}):[i("span",{staticClass:"error-text"},[e._v("Field "+e._s(t.slug)+" not found in serializer")])]],2)]}))],2)],1)]]:e._e()]}))],2)})),1)],1)},a=[],n=i("3835"),r=(i("caad"),i("4fad"),i("2532"),function(){var e=this,t=e.$createElement,i=e._self._c||t;return i("div",[e.getCustomField(e.formInfo.viewname,e.field_slug)?[i("keep-alive",[i(e.getCustomField(e.formInfo.viewname,e.field_slug),{ref:"field-element",tag:"component",attrs:{error:e.error,field:e.field,"field-slug":e.field_slug},on:{changed:e._updateValue}})],1)]:[i("el-form-item",{class:{"is-required":e.field.required},attrs:{label:e.label,prop:e.field_slug,"label-width":e.labelWidth}},["datetime"===e.field.type?i("el-date-picker",{ref:"field-element",class:e.field.type,attrs:{type:"datetime",placeholder:e.$t("select_datetime"),"value-format":"yyyy-MM-ddTHH:mm:ss",disabled:e.field.read_only},model:{value:e.fieldValue,callback:function(t){e.fieldValue=t},expression:"fieldValue"}}):"date"===e.field.type?i("el-date-picker",{ref:"field-element",class:e.field.type,attrs:{type:"date",placeholder:"$t('chose_date')","value-format":"yyyy-MM-dd",disabled:e.field.read_only},model:{value:e.fieldValue,callback:function(t){e.fieldValue=t},expression:"fieldValue"}}):e.types.choice.indexOf(e.field.type)>=0?i("div",[i("el-select",{ref:"field-element",class:e.field.type,attrs:{multiple:"multiple choice"===e.field.type,disabled:e.field.read_only},model:{value:e.fieldValue,callback:function(t){e.fieldValue=t},expression:"fieldValue"}},e._l(e.field.choices,(function(e){return i("el-option",{key:e.value,attrs:{label:e.display_name,value:e.value}})})),1)],1):e.types.string.indexOf(e.field.type)>=0?i("div",[e.field.wysiwyg?[i("fieldwysiwyg",{ref:"field-element",attrs:{field:e.field,"field-slug":e.field_slug,disabled:e.field.read_only,skin:e.settings.wysiwygSkin},on:{changed:e._updateValue}})]:[i("el-input",{ref:"field-element",staticClass:"string",attrs:{type:e.field.multilined?"textarea":"",maxlength:e.field.max_length,disabled:e.field.read_only,placeholder:e.placeholder},model:{value:e.fieldValue,callback:function(t){e.fieldValue=t},expression:"fieldValue"}})]],2):"integer"===e.field.type?i("el-input-number",{ref:"field-element",attrs:{min:e.field.min_value,max:e.field.max_value,name:e.field.type,disabled:e.field.read_only},model:{value:e.fieldValue,callback:function(t){e.fieldValue=t},expression:"fieldValue"}}):"decimal"===e.field.type?i("el-input-number",{ref:"field-element",attrs:{precision:e.precision,step:.1,min:e.field.mininternal_value,max:e.field.maxinternal_value,disabled:e.field.read_only},on:{change:e._updateValue},model:{value:e.fieldValue,callback:function(t){e.fieldValue=t},expression:"fieldValue"}}):"time"===e.field.type?i("el-time-picker",{ref:"field-element",class:e.field.type,attrs:{placeholder:e.$t("chose_time"),"value-format":"hh:mm:ss",disabled:e.field.read_only},model:{value:e.fieldValue,callback:function(t){e.fieldValue=t},expression:"fieldValue"}}):e.types.related.indexOf(e.field.type)>=0?i("div",{staticClass:"form-tags"},[i("tagsfield",{ref:"field-element",class:e.field.type,attrs:{"model-name":e.field.model_name,"app-label":e.field.app_label,viewname:e.formInfo.viewname,type:e.field.type,"max-tags":"primary"===e.field.type?1:null,placeholder:"primary"===e.field.type?e.$t("select_one_choice"):e.$t("select_choices"),disabled:e.field.read_only,add:!0,"api-info":e.apiInfo,"field-slug":e.field_slug,"init-form-data":e.initFormData,settings:e.settings,"instance-id":e.formInfo.recordId,"relation-name-filter":e.formInfo.relationNameFilter,"filter-id":e.formInfo.filterId},on:{changed:e._updateValue}})],1):"boolean"===e.field.type?i("el-switch",{ref:"field-element",class:e.field.type,attrs:{disabled:e.field.read_only},model:{value:e.fieldValue,callback:function(t){e.fieldValue=t},expression:"fieldValue"}}):e.types.file.indexOf(e.field.type)>=0?[i("filefield",{ref:"field-element",attrs:{field:e.field,"field-slug":e.field_slug},on:{changed:e._updateValue}})]:e.types.json.indexOf(e.field.type)>=0?[i("jsonfield",{ref:"field-element",attrs:{field:e.field,"field-slug":e.field_slug},on:{changed:e._updateValue}})]:["field"].indexOf(e.field.type)>=0?i("el-input",{ref:"field-element",staticClass:"string",attrs:{maxlength:e.field.max_length,disabled:e.field.read_only},model:{value:e.fieldValue,callback:function(t){e.fieldValue=t},expression:"fieldValue"}}):i("div",[e._v(e._s(e.field.type)+' "'+e._s(e.field.label)+'": '+e._s(e.fieldValue))]),e.field.help_text?i("span",{staticClass:"help-text"},[e._v(e._s(e.field.help_text))]):e._e(),e.error?i("div",{staticClass:"errors"},e._l(e.error,(function(t,l){return i("span",{staticClass:"error-text"},[e._v(" "+e._s(t)+" ")])})),0):e._e()],2),i("div",{staticClass:"el-form-item-delimiter"})]],2)}),s=[],o=(i("a9e3"),function(){var e=this,t=e.$createElement,i=e._self._c||t;return i("div",{staticClass:"json-editor"},[i("textarea",{ref:"textarea"})])}),d=[],c=(i("e9c4"),i("b64b"),i("56b3")),u=i.n(c);i("0dd0"),i("a7be"),i("acdf"),i("f9d4"),i("8822"),i("d2de");i("ae67");var f={name:"jsonfield",props:["field","fieldSlug"],data:function(e){return{jsonEditor:null,theme:"default"}},mounted:function(){this.$nextTick((function(){var e=this;this.jsonEditor=u.a.fromTextArea(this.$refs.textarea,{lineNumbers:!0,mode:"application/json",lint:!0,theme:this.theme}),this.jsonEditor.on("change",(function(t){e.$emit("changed",t.getValue())}))}))},methods:{updateFormData:function(e){var t=e[this.fieldSlug];try{t=JSON.stringify(JSON.parse(t),null,2)}catch(i){console.error('Json "'.concat(this.fieldSlug,'" error:'),i)}this.jsonEditor.setValue(t)}}},m=f,p=i("2877"),h=Object(p["a"])(m,o,d,!1,null,null,null),g=h.exports,b=i("b314"),y=function(){var e=this,t=e.$createElement,i=e._self._c||t;return i("div",{staticClass:"image-upload"},[i("div",{staticClass:"upload-info"},["svgfield"===e.field.type?[i("el-upload",{attrs:{action:"https://jsonplaceholder.typicode.com/posts/",accept:"image/svg+xml","show-file-list":!1,"on-success":e.handleAvatarSuccess,"before-upload":e.beforeAvatarUpload}},[i("label",{staticClass:"upload-button el-button el-button--primary"},[e._v(e._s(e.$t("select")))])])]:[i("label",{staticClass:"upload-button el-button el-button--primary",attrs:{for:e.inputId}},[e._v(e._s(e.$t("select")))]),i("input",{ref:"fileInput",class:e.field.type,attrs:{hidden:"",type:"file",id:e.inputId},on:{change:e.changeFile}})]],2),e.temp||e.defaultSVGComponent?["file upload"===e.field.type?i("el-link",{staticClass:"file-link",attrs:{href:e.temp,target:"_blank"}},[e._v(e._s(e.temp.slice(-80))+" ")]):e.temp?[i("div",{attrs:{hidden:""}},[e._v(e._s(e.temp))]),i("el-image",{staticClass:"image-field",attrs:{src:e.temp,href:e.temp}})]:e.defaultSVGComponent?i("div",{staticClass:"image-field",domProps:{innerHTML:e._s(e.defaultSVGComponent)}}):e._e(),i("i",{staticClass:"file-remove el-icon-delete",on:{click:e.removeFile}})]:e._e()],2)},v=[],_=(i("99af"),i("fb6a"),i("b0c0"),i("d3b7"),i("ac1f"),i("3ca3"),i("5319"),i("ad9d"),i("ddb0"),i("2b3d"),i("9861"),{name:"filefield",props:["field","fieldSlug"],data:function(e){return{temp:null,defaultSVGComponent:null,inputId:e.fieldSlug+(new Date).getTime()}},created:function(){this.setDefaultValue(this.initValue)},methods:{updateFormData:function(e){var t=e[this.fieldSlug];null!==this.temp&&void 0!==this.temp||this.setDefaultValue(t)},setDefaultValue:function(e){e&&(-1!==["image upload","file upload"].indexOf(this.field.type)?this.temp=e:"svgfield"===this.field.type&&(this.defaultSVGComponent=e))},toBase64:function(e){return new Promise((function(t,i){var l=new FileReader;l.readAsDataURL(e),l.onload=function(){return t(l.result)},l.onerror=function(e){return i(e)}}))},changeFile:function(e){var t=this,i=e.target.files[0];this.temp=URL.createObjectURL(i);var l=i.name.replaceAll(",","").slice(0,100);this.toBase64(i).then((function(e){var i="".concat(l,",").concat(e);t.$emit("changed",i)})).catch((function(e){var t="Error for convert file to base64 for ".concat(fieldSlug);console.error(t),Message({message:t,type:"error",duration:3e3})}))},removeFile:function(){this.temp=null,this.defaultSVGComponent=null,this.$refs.fileInput.value=null,this.$emit("changed",null)},handleAvatarSuccess:function(e,t){var i=this;this.temp=URL.createObjectURL(t.raw);var l=new FileReader;l.readAsText(t.raw),l.onload=function(){return i.$emit("changed",l.result)}},beforeAvatarUpload:function(e){var t="image/svg+xml"===e.type,i=e.size/1024<100;return t||this.$message.error("Icon picture must be SVG format!"),i||this.$message.error("Icon picture size can not exceed 100kb!"),t&&i}}}),w=_,k=Object(p["a"])(w,y,v,!1,null,null,null),x=k.exports,j=function(){var e=this,t=e.$createElement,i=e._self._c||t;return i("div",{staticClass:"tinymce-container",class:{fullscreen:e.fullscreen},style:{width:e.containerWidth}},[i("textarea",{staticClass:"tinymce-textarea",attrs:{id:e.tinymceId}}),e._v(" "),i("div",{staticClass:"editor-custom-btn-container"},[i("editorImage",{staticClass:"editor-upload-btn",attrs:{color:"#1890ff"},on:{successCBK:e.imageSuccessCBK}})],1)])},O=[],C=(i("00b4"),i("159b"),function(){var e=this,t=e.$createElement,i=e._self._c||t;return i("div",{staticClass:"upload-container"},[i("el-button",{style:{background:e.color,borderColor:e.color},attrs:{icon:"el-icon-upload",size:"mini",type:"primary"},on:{click:function(t){e.dialogVisible=!0}}},[e._v(" upload ")]),i("el-dialog",{attrs:{visible:e.dialogVisible},on:{"update:visible":function(t){e.dialogVisible=t}}},[i("el-upload",{staticClass:"editor-slide-upload",attrs:{multiple:!0,"file-list":e.fileList,"show-file-list":!0,"on-remove":e.handleRemove,"on-success":e.handleSuccess,"before-upload":e.beforeUpload,action:"https://httpbin.org/post","list-type":"picture-card"}},[i("el-button",{attrs:{size:"small",type:"primary"}},[e._v(" Click upload ")])],1),i("el-button",{on:{click:function(t){e.dialogVisible=!1}}},[e._v(" Cancel ")]),i("el-button",{attrs:{type:"primary"},on:{click:e.handleSubmit}},[e._v(" Confirm ")])],1)],1)}),V=[],S=(i("d81d"),{name:"EditorSlideUpload",props:{color:{type:String,default:"#1890ff"}},data:function(){return{dialogVisible:!1,listObj:{},fileList:[]}},methods:{checkAllSuccess:function(){var e=this;return Object.keys(this.listObj).every((function(t){return e.listObj[t].hasSuccess}))},handleSubmit:function(){var e=this,t=Object.keys(this.listObj).map((function(t){return e.listObj[t]}));this.checkAllSuccess()?(this.$emit("successCBK",t),this.listObj={},this.fileList=[],this.dialogVisible=!1):this.$message("Please wait for all images to be uploaded successfully. If there is a network problem, please refresh the page and upload again!")},handleSuccess:function(e,t){for(var i=t.uid,l=Object.keys(this.listObj),a=0,n=l.length;a<n;a++)if(this.listObj[l[a]].uid===i)return this.listObj[l[a]].url=e.files.file,void(this.listObj[l[a]].hasSuccess=!0)},handleRemove:function(e){for(var t=e.uid,i=Object.keys(this.listObj),l=0,a=i.length;l<a;l++)if(this.listObj[i[l]].uid===t)return void delete this.listObj[i[l]]},beforeUpload:function(e){var t=this,i=window.URL||window.webkitURL,l=e.uid;return this.listObj[l]={},new Promise((function(a,n){var r=new Image;r.src=i.createObjectURL(e),r.onload=function(){t.listObj[l]={hasSuccess:!1,uid:e.uid,width:this.width,height:this.height}},a(!0)}))}}}),I=S,$=(i("cd85"),Object(p["a"])(I,C,V,!1,null,"38be4040",null)),F=$.exports,T=i("b85c"),D=[];function q(){return window.tinymce}var E=function(e,t){var i=document.getElementById(e),l=t||function(){};if(!i){var a=document.createElement("script");a.src=e,a.id=e,document.body.appendChild(a),D.push(l);var n="onload"in a?r:s;n(a)}function r(t){t.onload=function(){this.onerror=this.onload=null;var e,i=Object(T["a"])(D);try{for(i.s();!(e=i.n()).done;){var l=e.value;l(null,t)}}catch(a){i.e(a)}finally{i.f()}D=null},t.onerror=function(){this.onerror=this.onload=null,l(new Error("Failed to load "+e),t)}}function s(e){e.onreadystatechange=function(){if("complete"===this.readyState||"loaded"===this.readyState){this.onreadystatechange=null;var t,i=Object(T["a"])(D);try{for(i.s();!(t=i.n()).done;){var l=t.value;l(null,e)}}catch(a){i.e(a)}finally{i.f()}D=null}}}i&&l&&(q()?l(null,i):D.push(l))},z=E,U=i("d369"),L=["advlist anchor autolink autosave code codesample colorpicker colorpicker contextmenu directionality emoticons fullscreen hr image imagetools insertdatetime link lists media nonbreaking noneditable pagebreak paste preview print save searchreplace spellchecker tabfocus table template textcolor textpattern visualblocks visualchars wordcount accordion"],R=["searchreplace undo redo | bold italic underline strikethrough blockquote removeformat | alignleft aligncenter alignright outdent indent | subscript superscript code codesample","hr bullist numlist link image charmap anchor pagebreak insertdatetime media table emoticons forecolor backcolor add-accordion | preview fullscreen"],A="".concat(U["a"].static_prefix,"/tinymce/tinymce.min.js"),B={name:"wysiwyg",components:{editorImage:F},props:{field:{type:Object},fieldSlug:{type:String},disabled:{type:Boolean,default:!1},toolbar:{type:Array,required:!1,default:function(){return[]}},skin:{type:String,required:!0,validator:function(e){return-1!==Object.keys(U["d"]).indexOf(e)}},theme:{type:String,default:"modern"},menubar:{type:String,default:"file edit insert view format table"},height:{type:[Number,String],required:!1,default:260},width:{type:[Number,String],required:!1,default:"auto"}},data:function(e){return{hasChange:!1,hasInit:!1,tinymceId:this.fieldSlug,fullscreen:!1,init_value:null}},computed:{containerWidth:function(){var e=this.width;return/^[\d]+(\.[\d]+)?$/.test(e)?"".concat(e,"px"):e}},mounted:function(){var e=this;z(A,(function(t){t?e.$message.error(t.message):e.initTinymce()}))},activated:function(){window.tinymce&&this.initTinymce()},deactivated:function(){this.destroyTinymce()},destroyed:function(){this.destroyTinymce()},methods:{updateFormData:function(e){var t=e[this.fieldSlug];window.tinymce?window.tinymce.get(this.tinymceId).setContent(t||""):this.init_value=t||""},init:function(){this.initTinymce()},initTinymce:function(){var e=this,t=this;window.tinymce.init({theme:this.theme,skin:this.skin,skin_url:"".concat(U["a"].static_prefix,"/tinymce/").concat(this.skin),external_plugins:{accordion:"".concat(U["a"].static_prefix,"/tinymce/plugins/accordion/plugin.js")},plugin_preview_width:"1200",plugin_preview_height:"800",selector:"#".concat(this.tinymceId),language:"en",height:this.height,body_class:"panel-body",object_resizing:!1,toolbar:this.toolbar.length>0?this.toolbar:R,menubar:this.menubar,plugins:L,end_container_on_empty_block:!0,powerpaste_word_import:"clean",code_dialog_height:450,code_dialog_width:1e3,advlist_bullet_styles:"square",advlist_number_styles:"default",imagetools_cors_hosts:["www.tinymce.com","codepen.io"],default_link_target:"_blank",link_title:!1,nonbreaking_force_tab:!0,init_instance_callback:function(i){t.init_value&&i.setContent(t.init_value),t.hasInit=!0,i.on("NodeChange Change KeyUp SetContent",(function(){e.hasChange=!0,e.$emit("changed",i.getContent())}))},setup:function(e){e.on("FullscreenStateChanged",(function(e){t.fullscreen=e.state}))},convert_urls:!1})},destroyTinymce:function(){var e=window.tinymce.get(this.tinymceId);this.fullscreen&&e.execCommand("mceFullScreen"),e&&e.destroy()},setContent:function(e){window.tinymce.get(this.tinymceId).setContent(e)},getContent:function(){window.tinymce.get(this.tinymceId).getContent()},imageSuccessCBK:function(e){var t=this;e.forEach((function(e){return window.tinymce.get(t.tinymceId).insertContent('<img class="wscnph" src="'.concat(e.url,'" >'))}))}}},G=B,M=Object(p["a"])(G,j,O,!1,null,null,null),N=M.exports,J=[{vuewname:"bonusfreespinsetting",fieldname:"freespin_config",field:function(){return i.e("chunk-ecedfa6a").then(i.bind(null,"2dd8"))}}];function K(e,t){var i,l=Object(T["a"])(J);try{for(l.s();!(i=l.n()).done;){var a=i.value;if(a.vuewname===e&&a.fieldname===t)return a.field}}catch(n){l.e(n)}finally{l.f()}}var P={name:"FieldElement",props:{settings:{type:Object,required:!0},field_slug:{type:String,required:!0},field:{type:Object,required:!0},precision:{type:Number,default:2},formInfo:{type:Object,required:!0},apiInfo:{type:Object,required:!0},labelWidth:{type:String,default:"230px"},label:{type:String,required:!1},initFormData:{required:!1},placeholder:{type:String,required:!1}},components:{tagsfield:b["a"],filefield:x,jsonfield:g,fieldwysiwyg:N},data:function(){return{types:{string:["string","email","url","slug"],choice:["list","choice","multiple choice"],related:["primary","primarymany"],file:["image upload","file upload","svgfield"],json:["json"]},getCustomField:K,typesMap:{integer:"number",string:"string",boolean:"boolean",email:"string",choice:"string"},internal_value:"",internal_error:null}},computed:{error:{get:function(){return this.internal_error},set:function(e){this.internal_error=e,this.$emit("update_error",e)}},fieldValue:{get:function(){return this.internal_value},set:function(e){this.internal_value!==e&&(this.internal_value=e,this.$emit("changed",e))}}},created:function(){this.updateFormData(this.initFormData)},methods:{updateFormData:function(e){var t=e[this.field_slug];this.types.string.indexOf(this.field.type)>=0&&null===t&&(t=""),this.internal_value=t;var i=this.$refs["field-element"];void 0!==i&&"function"===typeof i.updateFormData&&i.updateFormData(e)},updateError:function(e){this.error=e},_updateValue:function(e){this.fieldValue=e}}},W=P,H=Object(p["a"])(W,r,s,!1,null,null,null),Q=H.exports,X=(i("5f87"),{name:"FieldsContainer",props:{settings:{type:Object,required:!0},formInfo:{validator:function(e){return-1!==["create","update"].indexOf(e.formType)}},apiInfo:Object,meta:{type:Object,required:!1,validator:function(e){return null!=e.serializer||(console.error("fields-container meta must contain serializer"),!1)},default:function(e){return this.apiInfo[this.formInfo.viewname].meta}}},components:{fieldelement:Q},data:function(){return{formData:{},errors:{},apiMethods:null,temp:{},activeTab:0,translationsTabs:{}}},watch:{formData:{handler:function(e){e&&this.$emit("changed",e)},deep:!0}},methods:{getTranslations:function(){return this.meta.translations||{}},getGroups:function(){return this.meta.field_groups?this.meta.field_groups:[{title:""}]},isTranslation:function(e){for(var t=0,i=Object.entries(this.getTranslations());t<i.length;t++)for(var l=Object(n["a"])(i[t],2),a=(l[0],l[1]),r=0;r<a.length;r++)if(a[r].slug===e)return!0;return!1},canBeDisplayed:function(e,t,i){if("create"===this.formInfo.formType&&(e.read_only||e.update_only))return!1;if("create"!==this.formInfo.formType&&e.create_only)return!1;if(this.meta.field_groups&&null!==this.meta.field_groups){var l=this.meta.field_groups[i].fields;if(l&&!l.includes(t))return!1}return!0},updateErrors:function(e){this.errors=e;for(var t=0,i=Object.entries(this.meta.serializer);t<i.length;t++){var l=Object(n["a"])(i[t],2),a=l[0],r=(l[1],this.$refs["field_".concat(a)]);void 0!==r&&r[0].updateError(this.errors[a])}},updateFormData:function(e){this.formData=e;for(var t=0,i=Object.entries(this.meta.serializer);t<i.length;t++){var l=Object(n["a"])(i[t],2),a=l[0],r=(l[1],this.$refs["field_".concat(a)]);void 0!==r&&r[0].updateFormData(this.formData)}},_updateValue:function(e,t){this.$set(this.formData,t,e);for(var i=0,l=Object.entries(this.meta.serializer);i<l.length;i++){var a=Object(n["a"])(l[i],2),r=a[0],s=(a[1],this.$refs["field_".concat(r)]);void 0!==s&&(t!==r&&s[0].updateFormData(this.formData))}}}}),Y=X,Z=Object(p["a"])(Y,l,a,!1,null,null,null);t["default"]=Z.exports},cd85:function(e,t,i){"use strict";i("d78e")},d78e:function(e,t,i){}}]);