export const defaultProps = {
  field: {type: Object, required: true},
  fieldSlug: {type: String, required: true},
  viewname: {type: String, required: true},
}

const baseFields = [
  'type',
  'required',
  'read_only',
  'label',
  'help_text',
  'write_only',
  'update_only',
  'create_only',
  'initial',
]

export function validateProps(comp, compReqFields) {
  for (const fieldName of baseFields.concat(compReqFields || [])) {
    if (Object.keys(comp.field).indexOf(fieldName) === -1) {
      console.warn(`Field ${comp.viewname}.${comp.fieldSlug} field attribute not found: "${fieldName}"`)
    }
  }
}
