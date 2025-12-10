<template>
	<div class="casePhotosUpload">
		<div class="casePhotosUpload__head">
			<h5>Upload Case Photos to Get Started</h5>
			<p>Lorem Ipsum is simply dummy text of the printing industry.</p>
		</div>
		<div class="casePhotosUpload__body">
			<div class="grid" data-grid-item-width="1/6">
				<div
					class="grid__item"
					v-for="index in 18"
					:key="index"
					@click="openUpload"
				>
					<input type="file" name="file" @change="upload" />
					<div class="grid__item--name">
						Lateral Ceph
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
export default {
	methods: {
		upload: function (e) {
			let wrapper = e.target.parentNode;
			wrapper.classList.add("upload");
			let img = wrapper.querySelector("img");
			if(img){
				img.remove();
			}
			img = document.createElement('img');
			img.src = URL.createObjectURL(e.target.files[0]);
			wrapper.appendChild(img)
		},
	},
};
</script>

<style lang="scss" scoped>
.casePhotosUpload {
	padding: rem(24px);
	&__head {
		margin-bottom: rem(24px);
		h5 {
			margin-bottom: rem(6px);
		}
	}
	&__body {
		.grid {
			$self: &;
			display: grid;
			grid-template-columns: repeat(6, 1fr);
			grid-gap: 16px;
			&__item {
				$self: &;
				transition: 0.5s ease-in-out;
				cursor: pointer;
				border-radius: 8px;
				overflow: hidden;
				width: 100%;
				height: 170px;
				&:after{
					content:"";
					position:absolute;
					height:100%;
					width:100%;
					border: 2px dashed #c9c9c9;
					left:0;
					top:0;
					border-radius: 8px;
					overflow: hidden;
				}
				input[type='file']{
					z-index:3;
				}
				::v-deepimg {
					width: 100%;
					height: 100%;
				}
				&--name {
					position: absolute;
					left: 50%;
					top: 50%;
					transform: translate(-50%, -50%);
					width: 100%;
					color: #8e8e8e;
					font-size: rem(14px);
					font-weight: 500;
					text-align: center;
					transition: 0.4s ease-in;
					z-index: 2;
				}
				&.upload {
					#{ $self }--name {
						color: #fff;
					}
					@media screen and (min-width:1025px){
						&:hover{
							&:before{
								content:"";
								position:absolute;
								height:100%;
								width:100%;
								background:rgba($color: #171716, $alpha: .8);
								border-radius: 8px;
								left: 0px;
								top: 0px;
								transition: 0.5s ease-in-out;
							}
							&:after{
								z-index:-1;
							}
						}
					}
					.grid__item--name {
						color: #fff;
					}
				}
				&:hover {
					&:before {
						opacity: 1;
					}
				}
			}
		}
		@media screen and (max-width:991px){
			.grid{
				grid-template-columns: repeat(5, 1fr);
				&__item{
					height:150px;
				}
			}
		}
		@media screen and (max-width:767px){
			.grid{
				grid-template-columns: repeat(4, 1fr);
			}
		}
		@media screen and (max-width:600px){
			.grid{
				grid-template-columns: repeat(3, 1fr);
				&__item{
					height:125px;
				}
			}
		}
		@media screen and (max-width:500px){
			.grid{
				grid-template-columns: repeat(2, 1fr);
			}
		}
	}
}
</style>
