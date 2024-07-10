import FSSettings from '/src/components/custom-fields/FSSettings.vue'

const fields = [
    {
        'vuewname': 'bonusfreespinsetting',
        'fieldname': 'freespin_config',
        'field': FSSettings,
    },
]


export function getCustomField(vuewname, fieldname) {
    for (const field_info of fields) {
        if (field_info.vuewname === vuewname && field_info.fieldname === fieldname) {
            return field_info.field
        }
    }
}
