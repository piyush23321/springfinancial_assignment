/** @odoo-module */

import { CharField, charField } from "@web/views/fields/char/char_field";
import { registry } from "@web/core/registry";
import { patch } from "@web/core/utils/patch";
import {Many2XAutocomplete,} from "@web/views/fields/relational_utils";
import { AutoComplete } from "@web/core/autocomplete/autocomplete";


import { useService } from "@web/core/utils/hooks";

// ---------test code------------
export class ApplicantCharField extends CharField {
    static template = "char_field.ApplicantCharField";
    setup() {
        super.setup();
    }
}

export const applicantCharField = {
    ...charField,
    component: ApplicantCharField,
};

registry.category("fields").add("applicant_char", applicantCharField);
// end of test code

// -----------------------------------------------------------------------------------
patch(AutoComplete.prototype, {
    selectOption(indices, params = {}) {
        var option = this.sources[indices[0]].options[indices[1]];
        var selected_fields = $('.dropdown-menu.ui-autocomplete.show').find('input:checked');
        var self = this;
        selected_fields.each(function (index, element) {
            option =  $.grep(self.sources[0].options, function(obj) {
                return obj.id == parseInt(element.id);
            })[0]
            option = {'value':option.id,'displayName':option.displayName}
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
})