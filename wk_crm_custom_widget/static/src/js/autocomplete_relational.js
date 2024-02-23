/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Many2XAutocomplete } from "@web/views/fields/relational_utils";
import { patch } from "@web/core/utils/patch";
import { AutoComplete } from "@web/core/autocomplete/autocomplete";


import { Many2ManyTagsField, many2ManyTagsField } from "@web/views/fields/many2many_tags/many2many_tags_field";
Many2XAutocomplete.props = { ...Many2XAutocomplete.props, nocustommany2many: { type: Boolean, optional: true } }

export class CustomMany2ManyTagsField extends Many2ManyTagsField {
    static template = "crm_field_customization.Many2ManyTagsField";
    setup() {
        super.setup();
    }
}

export const customMany2ManyTagsField = {
    ...many2ManyTagsField,
    component: CustomMany2ManyTagsField,
};

registry.category("fields").add("custom_many2many_tags", customMany2ManyTagsField);


patch(AutoComplete.prototype, {
    setup() {
        super.setup();
        this.selectedRecords = [];
    },

    addRecordData(ev) {
        if ($(ev.currentTarget).prop('checked')) {
            this.selectedRecords.push(parseInt($(ev.currentTarget).attr('id')))
        }
        else {
            this.selectedRecords.pop(parseInt($(ev.currentTarget).attr('id')))
        }
    },

    optionCheckpoint(option){
        !this.props.dirtyOption.includes(option) ? this.props.dirtyOption.push(option) : ''
    },

    is_custom_widgetFun(val,option){
        if(val){
            this.props.is_custom_widget = val;
        }
        else{
            this.props.dirtyOption ? this.optionCheckpoint(option) : this.props.dirtyOption =[option]
        }
    },

    open(useInput = false) {
        this.selectedRecords = [];
        return super.open(...arguments);
    },

    selectOption(indices, params = {}) {
        if (this.props.is_custom_widget && !this.props.dirtyOption.includes(indices[1])) {
            if(!this.selectedRecords.length){
                return;
            }
            var self = this;
            this.selectedRecords.forEach( (element) => {
                var option = $.grep(self.sources[0].options, function(obj) {
                    return obj.id == element;
                })[0]
                self.inEdition = false;
                if (option.unselectable) {
                    self.inputRef.el.value = "";
                    self.close();
                    return;
                }

                if (self.props.resetOnSelect) {
                    self.inputRef.el.value = "";
                }

                self.forceValFromProp = true;
                self.props.onSelect(option, {
                    ...params,
                    input: self.inputRef.el,
                });
            });

            this.close();
        }
        else {
            return super.selectOption(...arguments);
        }
    }
})