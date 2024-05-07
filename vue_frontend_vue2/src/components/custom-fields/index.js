
const fields = [
    {
        'vuewname': 'bonusfreespinsetting',
        'fieldname': 'freespin_config',
        'field': () => import('@/components/custom-fields/freespins-settings'),
    },
]


export function getCustomField(vuewname, fieldname) {
    for (const field_info of fields) {
        if (field_info.vuewname === vuewname && field_info.fieldname === fieldname) {
            return field_info.field
        }
    }
}
