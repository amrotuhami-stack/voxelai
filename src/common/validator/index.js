import {coutryCodes} from "../constant/countryCodes"
const AppValidator = {
    addNewPatient: (form) => {
        var errors = [];
        if(!form.patientFirstName) {
            errors.push("Patient's first name required !")
        }
        else if(form.patientFirstName.length < 4) {
            errors.push("Patient's first name must be at least 4 characters !")
        }
        if(!form.patientLastName) {
            errors.push("Patient's last name required !")
        }
        else if(form.patientLastName.length < 4) {
            errors.push("Patient's last name must be at least 4 characters !")
        }
        if(!form.patientGender) {
            errors.push("Patient's Gender required !")
        }
        var regex = /[0-9]|\./;
        if(!form.patientAge) {
            errors.push("Patient's age required !")
        }
        else if( !regex.test(form.patientAge) ) {
            errors.push("Patient's age must be numeric !")
        }
        return errors
    },

    billingAndShippingAddress: (form, input) => {
        var errors = [];
        if(!form.firstName) {
            errors.push({
                key: "first_name",
                type: "required",
                messege: "First name required !"
            })
        }
        else if(form.firstName.length < 3) {
            errors.push({
                key: "first_name",
                type: "min-length",
                messege: "First name must be at least 3 characters !"
            })
        }
        if(input == 'first_name') return errors;
        if(!form.lastName) {
            errors.push({
                key: "last_name",
                type: "required",
                messege: "Last name required !"
            })
        }
        else if(form.lastName.length < 3) {
            errors.push({
                key: "last_name",
                type: "min-length",
                messege: "Last name must be at least 3 characters !"
            })
        }
        if(input == 'last_name') return errors;
        if(!form.emailAddress) {
            errors.push({
                key: "email_address",
                type: "required",
                messege: "Your's e-mail address required !"
            })
        }
        if(input == 'email_address') return errors;
        if(form.invalidPhoneNumber == "billing" || form.invalidPhoneNumber == "shipping") {
            errors.push({
              key: "phone_number",
              type: "invalid",
              messege: "Your's phone number invaild"
            })
        }
        else if(!form.phoneNumber) {
            errors.push({
                key: "phone_number",
                type: "required",
                messege: "Your's phone number required !"
            })
        }
        else if(!form.phoneNumber.includes('+' + coutryCodes[form.countryCode])) {
            errors.push({
                key: "phone_number",
                type: "country-code-check",
                messege: "Your's phone number invaild (country code required)"
            })
        }
        if(input == 'phone_number') return errors;
        if(!form.country) {
            errors.push({
                key: "country",
                type: "required",
                messege: "Your's country required !"
            })
        }
        if(input == 'country') return errors;
        if(!form.city) {
            errors.push({
                key: "city",
                type: "required",
                messege: "Your's city required !"
            })
        }
        if(input == 'city') return errors;
        if(!form.address) {
            errors.push({
                key: "address",
                type: "required",
                messege: "Your's address required !"
            })
        }
        if(input == 'address') return errors;
        return errors
    },
    personalInfo: (form) => {
        var errors = [];
        if(!form.firstName) {
            errors.push({
                key: "first_name",
                type: "required",
                messege: "First name required !"
            })
        }
        else if(form.firstName.length < 3) {
            errors.push({
                key: "first_name",
                type: "min-length",
                messege: "First name must be at least 3 characters !"
            })
        }
        if(!form.lastName) {
            errors.push({
                key: "last_name",
                type: "required",
                messege: "Last name required !"
            })
        }
        else if(form.lastName.length < 3) {
            errors.push({
                key: "last_name",
                type: "min-length",
                messege: "Last name must be at least 3 characters !"
            })
        }
        if(!form.emailAddress) {
            errors.push({
                key: "email_address",
                type: "required",
                messege: "Your's e-mail address required !"
            })
        }
        if(!form.phoneNumber) {
            errors.push({
                key: "phone_number",
                type: "required",
                messege: "Your's phone number required !"
            })
        }
        else if(!form.phoneNumber.includes('+' + coutryCodes[form.countryCode])) {
            errors.push({
                key: "phone_number",
                type: "country-code-check",
                messege: "Your's phone number invaild (country code required)"
            })
        }
        return errors
    }
}

export default AppValidator