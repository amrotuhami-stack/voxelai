<template>
	<div>
		<div class="uploadFile" :class="fileDefinition.slug">
			<input type="file" :name="fileDefinition.slug" @change="upload" />
			<div class="uploadFile__desc">
				<h5>{{ fileDefinition.name }}
					<span>{{ fileDefinition.is_required == true ? '(Required)' : '(Optional)'}}</span>
				</h5>
				<p class="uploadFile__desc--subtitle" v-if="!file">
					Click here, to select your file
				</p>
				<p class="d-none uploadFile__desc--uploaded" v-if="uploadAt && file">
					<span id="date-time">{{ file.value.name + ' ( ' + Math.ceil(file.value.size / 1024) + ' KB )' + " - "}}</span> Uploaded at <span id="date-time">{{uploadAt}}</span>
				</p>
				<p class="d-none uploadFile__desc--uploaded" v-if="progress > 0 && file">
					<span id="date-time">{{ file.value.name + " - "}}</span> Uploading Progress <span id="date-time">{{ Math.ceil((progress / file.value.size) * 100) + " %" }}</span>  
				</p>
				<span v-if="file">
					<div class="serviceRow__cases--progress">
                		<b-progress
							v-if="progress > 0"
                  			:value="progress"
                  			:max="file.value.size"
                		/>
              		</div>
				</span>
			</div>
			<div class="uploadFile__action" v-if="!readOnly">
				<span v-if="progress == 0 && !file">
					<svg-icon
						icon-id="fileupload"
						icon-viewbox="0 0 24 24"
					></svg-icon>
				</span>
				<span class="d-none remove-icon" :class="fileDefinition.slug">
					<div v-if="progress > 0">
						<font-awesome-icon id="spinner" class="spinner" icon="spinner" size="1x" spin  />
					</div>
					<svg-icon
						icon-id="cross-icon"
						icon-viewbox="0 0 18 18"
						v-if="progress == 0 && file"
					></svg-icon>
				</span>
			</div>
		</div>
	</div>
</template>

<script>

import { ServiceHelper } from '@/common/crud-helpers/service';
import { mapGetters } from 'vuex';

export default {
	props: {
		fileDefinition: Object,
		uploadFile: {
      		type: Function,
      		default: () => {},
    	},
		removeFile: {
      		type: Function,
      		default: () => {},
    	},
		uploaded: {
      		type: Boolean,
      		default: false,
    	},
		readOnly: {
      		type: Boolean,
      		default: false,
    	},
	},
	data(){
		return {
			file: null,
			uploadAt: null,
			progress: 0
		}
	},
	computed: {
		...mapGetters(['loading', 'uploadProgress']),
	},
	watch: {
		uploaded() {
			if(this.uploaded && this.fileDefinition) {
				let upload = document.querySelector('.uploadFile.' + this.fileDefinition.slug);
				upload.classList.add('uploaded');
			}
		},
		uploadProgress() {
			if(this.file && this.file.name == this.uploadProgress.target) {
				this.uploadProgress.value >= this.file.value.size
					? this.progress = 0
					: this.progress = this.uploadProgress.value
			}
		}
	},
	methods: {
		upload(event) {
			if(!this.readOnly) {
				let upload = document.querySelector('.uploadFile.' + event.srcElement.name);
				upload.classList.add('uploaded');
				let close = document.querySelector('.remove-icon.' + event.srcElement.name);
				close.addEventListener('click', () => {
					upload.classList.remove('uploaded');
					this.removeFile({...this.fileDefinition})
					this.file = null
				});
				this.file = {...this.fileDefinition, value: event.target.files[0]}
				ServiceHelper.pushTempFile(this.file).then((resp) => {
					this.uploadFile({...this.file, temp_file_id: resp.temp_file_obj_id})
					var currentdate = new Date();
					this.uploadAt = currentdate.getDay() + "/" + currentdate.getMonth()
						+ "/" + currentdate.getFullYear() + " - "
						+ currentdate.getHours() + ":"
						+ currentdate.getMinutes() + ":" + currentdate.getSeconds();
				})
			}
		},
	},
};
</script>

<style lang="scss" scoped>
.uploadFile {
	$parent: &;
	margin-bottom: rem(15px);
	border: 2px dashed #e9e9e9;
	border-radius: 12px;
	display: flex;
	align-items: center;
	justify-content: space-between;
	padding: rem(24px);
	position: relative;
	cursor: pointer;
	&__desc {
		width: 80%;
		h5 {
			font-size: rem(16px);
			text-transform: capitalize;
			span {
				color: var(--textSecondary);
				font-size: rem(12px);
				padding-left: 8px;
				font-weight: normal;
			}
		}
		p {
			margin-bottom: 0 !important;
			color: var(--textSecondary) !important;
			font-size: rem(12px) !important;
		}
	}
	&__action {
		span {
			svg {
				width: 24px;
				height: 24px;
			}
		}
	}
	input[type='file'] {
		cursor: pointer;
	}
	&.uploaded {
		background: #eef7fb;
		border-color: #eef7fb;
		input[type='file'] {
			display: none;
			visibility: hidden;
			opacity: 0;
			width: 0;
			height: 0;
			font-size: 0;
			z-index: -9999999999999;
			appearance: none;
		}
		#{ $parent }__desc {
			#{ $parent }__desc--subtitle {
				display: none;
			}
			#{ $parent }__desc--uploaded {
				display: block !important;
			}
		}
		#{ $parent }__action {
			span {
				display: none;
				&.d-none {
					display: block !important;
				}
				svg {
					width: 24px;
					height: 24px;
				}
			}
		}
	}
}
</style>