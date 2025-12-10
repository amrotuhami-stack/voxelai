<template>
	<div>
		<div class="downloadFile" v-if="file">
			<div class="downloadFile__desc">
				<h5>{{ fileName }}
					<span> {{ '(Required) ' }} </span>
				</h5>
				<!-- <p class="uploadFile__desc--subtitle">
					Sit magna sodales urna.
				</p> -->
				<p class="downloadFile__desc" v-if="file.modified">
					Uploaded at <span id="date-time">{{ " " + file.modified.split('T')[0] + " | " +  file.modified.split('T')[1].split('.')[0] }}</span>
				</p>
			</div>
			<div class="downloadFile__action" v-if="downloadUrl">
				<a :href="downloadUrl" target = "_blank">
					<span>
						<svg-icon
							icon-id="filedownload"
							icon-viewbox="0 0 24 24"
						></svg-icon>
					</span>
				</a>
			</div>
		</div>
	</div>
</template>

<script>
// [*] Vuex State Getter And Action Helper
import { ServiceHelper } from '@/common/crud-helpers/service';

export default {
	props: {
		fileName: String,
		files:  {
      		type: Array,
      		default: [],
    	},
		photonFile: Object
	},
	data(){
		return {
			file: null,
			downloadUrl: null,
			error: null,
		}
	},
	created() {
		let index = this.files.findIndex((file) => file.name == this.fileName)
		if(index != -1) {
			this.file = this.files[index]
			ServiceHelper.getFileSignture({fileId: this.file.id}).then((file) => {
				this.downloadUrl = file.file
			})
		}

		/// [Important] Service from Photon File
		if(this.photonFile) {
			this.downloadUrl = this.photonFile.value
			this.file = this.photonFile
		}
	}
};
</script>

<style lang="scss" scoped>
.downloadFile {
	$parent: &;
    background-color: #F5F5F5;
	margin-bottom: rem(15px);
	border-radius: 12px;
	display: flex;
	align-items: center;
	justify-content: space-between;
	padding: rem(24px);
	position: relative;
	cursor: pointer;
	&__desc {
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


/*
// fileUpload: function () {
		// 	let upload = document.querySelector('.uploadFile');
		// 	let close = document.querySelector('.remove-icon');
		// 	let element = document.querySelector('input[type="file"]');
		// 	let file = document.querySelector('.uploadFile input[type="file"]');
		// 	// file.addEventListener('change', (e) => {
		// 	// 	upload.classList.add('uploaded');
		// 	// });
		// 	// close.addEventListener('click', () => {
		// 	// 	upload.classList.remove('uploaded');
		// 	// 	// element.parentNode.removeChild(element);
		// 	// });
		// },
		// myClock: function () {
		// 	setTimeout(function () {
		// 		const d = new Date();
		// 		const n = d.toLocaleTimeString();
		// 		document.getElementById('date-time').innerHTML = d;
		// 	}, 1000);
		// },
let formData = new FormData()
			// save vue instance for being able to reference it later.
			const vm = this;
			formData.append("file", event.target.files[0])
			ApiService.djfile(formData)
				.then(({ data }) => {
				// save details on the form data which will be sent to the server
				vm.files[event.target.name] = data;
				
				vm.$store.commit(SERVICE.UPDATE_UPLOADED_FILES, vm.files);
				})
				.catch((error) => {
					// remove the file from the input
					event.target.value = null
					// vm.error(error)
				})
 */