<template>
	<!-- invite doctor modal -->
		<b-modal
			class="inviteDoctor"
			ref="my-modal"
			id="invite-doctor"
			centered
		>
			<div class="modal-title">Invite Doctors to Voxel3Di</div>
			<p>The more doctors you invite, the more commission you get!</p>
			<form>
				<label for="doctor-email"
					>Invite by entering doctor’s email address</label
				>
				<div class="form-group">
					<input
						type="email"
						id="doctor-email"
						class="form-control"
						placeholder="Doctor’s Email Address"
					/>
					<button type="submit" class="btn btn-default">
						Invite
					</button>
				</div>
				<label for="copy-link"
					>or copy link to share via social community</label
				>
				<div class="form-group link">
					<input
						type="text"
						id="copy-link"
						class="form-control"
						placeholder="Doctor’s Email Address"
						value="https://voxel3di.com/invite/14472838sdfwf987089798"
					/>
					<button @click="copyLink" class="btn btn-primary">
						Copy
					</button>
				</div>
			</form>
		</b-modal>
		<!-- modal -->
</template>

<script>
export default {
	methods: {
		hideModal() {
			this.$refs['my-modal'].hide();
		},
		copyLink() {
			let copyText = document.getElementById('copy-link');

			copyText.select();
			copyText.setSelectionRange(0, 99999);

			navigator.clipboard.writeText(copyText.value);
		},
	},
};
</script>

<style lang="scss" scoped>
::v-deep #invite-doctor {
	form {
		label {
			margin-bottom: 10px;
		}
	}
	.form-group {
		margin: 0;
		margin-bottom: rem(24px);
		background: var(--imageBg);
		display: flex;
		align-items: center;
		padding: 7px 7px 7px 22px;
		border-radius: 12px;
		.btn {
			padding: rem(10px) rem(46px);
			border-radius: 8px;
		}
		a {
			padding-right: rem(16px);
		}
		.form-control {
			background: transparent;
			padding: 0;
			height: 40px;
			padding-right: rem(22px);
			&:focus{
				border:transparent;
				box-shadow: none;
				outline: none;
			}
			&::placeholder {
				display: block !important;
				opacity: 1 !important;
				color: #8e8e8e;
			}
		}
		@media screen and (max-width:500px){
			flex-direction: column;
			background:transparent;
			padding:0;
			.form-control{
				background: var(--imageBg);
				padding-left:rem(20px);
				padding-right:rem(20px);
			}
			.btn{
				height:40px;
				margin-top:rem(20px);
			}
		}
		&.link {
			margin: 0;
			padding-top:0;
			padding-bottom:0;
			display: flex;
			align-items: center;
			.form-control {
				font-weight: 400;
				color: var(--textSecondary);
			}
			button {
				padding: 0;
				color: var(--secondary);
				background: unset;
				border: 0;
				height: 48px;
				border-radius: 12px;
				min-width: auto;
				padding-right: 24px;
				@media screen and (max-width:500px){
					height:auto;
				}
			}
		}
	}
	.form-control {
		padding-top: 12px;
		&::placeholder {
			opacity: 1 !important;
		}
	}
}
</style>
