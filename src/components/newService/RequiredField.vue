<template>
	<div class="mt-3 mb-3">
		<div  v-for="(collection, cindex) in fields" :key="collection.id">
            <div class="inner-title" style="text-transform: capitalize;">
			    {{collection.title + ' required fields'}}
			    <svg-icon
					v-if="!readOnly"
			    	v-b-tooltip.hover
			    	:title="collection.title"
			    	icon-id="info-circle"
			    	icon-viewbox="0 0 24 24"
			    ></svg-icon>
			</div>
			<form v-for="(field, findex) in collection.required_fields" :key="field.slug">
				<div v-if="field.field_type == 'selec'" class="form-group no-label">
					<b-form-select
                        v-model="modelList[getIndexOfVModel(cindex, findex)]"
						:options="[
                            { value: null, text: field.name, disabled: true},
                            ...genrateOptionList(field.optionset.options),
                        ]"
                        :disabled="readOnly"
						style="text-transform: capitalize;"
					></b-form-select>
				</div>
				<div v-else class="form-group" >
					<textarea class="form-control" v-model="modelList[getIndexOfVModel(cindex, findex)]" :readonly="readOnly"></textarea>
					<label class="control-label">{{field.name}} <span  class="required" v-if="field.is_required">(Required)</span> </label>
				</div>
			</form>
		</div>
	</div>
</template>

<script>
// [*] Vuex State Getter And Action Helper
import { ServiceHelper } from '@/common/crud-helpers/service';
import { mapGetters } from 'vuex';

// [*] Import form validator
import AppValidator from "@/common/validator"

export default {
	props: {
        fields: Array,
		service: Object,
		readOnly: {
      		type: Boolean,
      		default: false,
    	},
		updateService: {
      		type: Function,
      		default: () => {},
    	},
	},
	data() {
		return {
            lengthOfCollections: [],
            modelList: [],
		};
	},
	computed: {
        ...mapGetters(['patients']),
    },

	mounted() {
		if(this.service && 'service_data' in this.service && this.service.service_data != null) {
			let models = []
            this.service.service_data.fields.forEach((collection) => {
                this.lengthOfCollections = [...this.lengthOfCollections, collection.required_fields.length]
                collection.required_fields.forEach((field) => models.push(field.value))
            })
            this.modelList = [...models]
		}
		else {
        	let models = []
        	this.fields.forEach((collection) => {
        	    this.lengthOfCollections = [...this.lengthOfCollections, collection.required_fields.length]
        	    collection.required_fields.forEach((field) => models.push(null))
        	})
        	this.modelList = [...models]
		}
	},
	watch: {
        modelList() {
            let updatedFields =  this.fields.map((collection, c) => {
                return {
                    ...collection,
                    required_fields: collection.required_fields.map((field, f) => {
                        return {...field, value: this.modelList[this.getIndexOfVModel(c, f)]}
                    }),
                }
            })
            this.updateService({fields: [...updatedFields]})
        },
		service() {
			
        }
    },
	methods: {
        genrateOptionList(options) {
            let list = []
            options.forEach((item) => {
                list.push({
					value: item.name, text: item.name
				})
            })
            return list
        },
        getIndexOfVModel(cindex, findex) {
            let sum = 0;
            for(let i = 0; i < cindex; i++) {
                sum = sum  + this.lengthOfCollections[i]
            }
            return sum + findex
        },
	}
};
</script>

<style lang="scss" scoped>
.contentBox {
	border-radius: 12px;
	padding-bottom: 7px;
	@media screen and (max-width: 991px) {
		border: 0;
		padding: 0;
	}
	.add-patient {
		margin-left: 26px;
		color: #8e8e8e;
	}
	.required {
		font-size: rem(11px);
		font-weight: normal;
	}
}

.errors {
		p {
			margin-bottom: rem(10px);
		}
		ul {
			list-style-type: none;
			margin-bottom: rem(15px);
			li {
				padding-left: rem(10px);
				margin-bottom: rem(10px);
				color: var(--orange);
			}
		}
	}
</style>
