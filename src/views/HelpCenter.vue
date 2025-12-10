<template>
	<div class="helpCenter">
		<base-bread-crumb :items="breadCrumbsItems"></base-bread-crumb>
		<div class="container">
			<h1 class="main-title">Help Center</h1>
			<p>How can we help?</p>
			<div class="search no-label form-group">
				<input
					type="text"
					class="form-control"
					placeholder="Enter your search term..."
				/>
			</div>
			<p>or choose a category to quickly find the help you need</p>
			<div>
				<b-tabs pills>
					<b-tab title="Getting Started" active>
						<div>
							<h3>Getting Started</h3>
							<div class="accordion" role="tablist">
								<b-card no-body>
									<b-card-header
										header-tag="header"
										role="tab"
									>
										<b-button
											block
											v-b-toggle.gettingStart1
											variant="info"
											>Do I need to make a
											payment?</b-button
										>
									</b-card-header>
									<b-collapse
										id="gettingStart1"
										visible
										accordion="my-accordion"
										role="tabpanel"
									>
										<b-card-body>
											<b-card-text
												><p>
													Lorem Ipsum is simply dummy
													text of the printing and
													typesetting industry. Lorem
													Ipsum has been the
													industry's standard dummy
													text ever since the 1500s,
													when an unknown printer took
													a galley of type and
													scrambled it to make a type
													specimen book. It has
													survived not only five
													centuries, but also the leap
													into electronic typesetting,
													remaining essentially
													unchanged. It was
													popularised in the 1960s
													with the release of Letraset
													sheets containing Lorem
													Ipsum passages, and more
													recently with desktop
													publishing software like
													Aldus PageMaker including
													versions of Lorem Ipsum.
												</p></b-card-text
											>
										</b-card-body>
									</b-collapse>
								</b-card>
								<b-card no-body>
									<b-card-header
										header-tag="header"
										role="tab"
									>
										<b-button
											block
											v-b-toggle.gettingStart2
											variant="info"
											>Do I need to make a
											payment?</b-button
										>
									</b-card-header>
									<b-collapse
										id="gettingStart2"
										visible
										accordion="my-accordion"
										role="tabpanel"
									>
										<b-card-body>
											<b-card-text
												><p>
													Lorem Ipsum is simply dummy
													text of the printing and
													typesetting industry. Lorem
													Ipsum has been the
													industry's standard dummy
													text ever since the 1500s,
													when an unknown printer took
													a galley of type and
													scrambled it to make a type
													specimen book. It has
													survived not only five
													centuries, but also the leap
													into electronic typesetting,
													remaining essentially
													unchanged. It was
													popularised in the 1960s
													with the release of Letraset
													sheets containing Lorem
													Ipsum passages, and more
													recently with desktop
													publishing software like
													Aldus PageMaker including
													versions of Lorem Ipsum.
												</p></b-card-text
											>
										</b-card-body>
									</b-collapse>
								</b-card>
								<b-card no-body>
									<b-card-header
										header-tag="header"
										role="tab"
									>
										<b-button
											block
											v-b-toggle.gettingStart3
											variant="info"
											>Do I need to make a
											payment?</b-button
										>
									</b-card-header>
									<b-collapse
										id="gettingStart3"
										visible
										accordion="my-accordion"
										role="tabpanel"
									>
										<b-card-body>
											<b-card-text
												><p>
													Lorem Ipsum is simply dummy
													text of the printing and
													typesetting industry. Lorem
													Ipsum has been the
													industry's standard dummy
													text ever since the 1500s,
													when an unknown printer took
													a galley of type and
													scrambled it to make a type
													specimen book. It has
													survived not only five
													centuries, but also the leap
													into electronic typesetting,
													remaining essentially
													unchanged. It was
													popularised in the 1960s
													with the release of Letraset
													sheets containing Lorem
													Ipsum passages, and more
													recently with desktop
													publishing software like
													Aldus PageMaker including
													versions of Lorem Ipsum.
												</p></b-card-text
											>
										</b-card-body>
									</b-collapse>
								</b-card>
							</div>
							<h3>Pricing & Plans</h3>
							<div class="accordion" role="tablist">
								<b-card no-body>
									<b-card-header
										header-tag="header"
										role="tab"
									>
										<b-button
											block
											v-b-toggle.pricePlan1
											variant="info"
											>Do I need to make a
											payment?</b-button
										>
									</b-card-header>
									<b-collapse
										id="pricePlan1"
										visible
										accordion="my-accordion"
										role="tabpanel"
									>
										<b-card-body>
											<b-card-text
												><p>
													Lorem Ipsum is simply dummy
													text of the printing and
													typesetting industry. Lorem
													Ipsum has been the
													industry's standard dummy
													text ever since the 1500s,
													when an unknown printer took
													a galley of type and
													scrambled it to make a type
													specimen book. It has
													survived not only five
													centuries, but also the leap
													into electronic typesetting,
													remaining essentially
													unchanged. It was
													popularised in the 1960s
													with the release of Letraset
													sheets containing Lorem
													Ipsum passages, and more
													recently with desktop
													publishing software like
													Aldus PageMaker including
													versions of Lorem Ipsum.
												</p></b-card-text
											>
										</b-card-body>
									</b-collapse>
								</b-card>
								<b-card no-body>
									<b-card-header
										header-tag="header"
										role="tab"
									>
										<b-button
											block
											v-b-toggle.pricePlan2
											variant="info"
											>Do I need to make a
											payment?</b-button
										>
									</b-card-header>
									<b-collapse
										id="pricePlan2"
										visible
										accordion="my-accordion"
										role="tabpanel"
									>
										<b-card-body>
											<b-card-text
												><p>
													Lorem Ipsum is simply dummy
													text of the printing and
													typesetting industry. Lorem
													Ipsum has been the
													industry's standard dummy
													text ever since the 1500s,
													when an unknown printer took
													a galley of type and
													scrambled it to make a type
													specimen book. It has
													survived not only five
													centuries, but also the leap
													into electronic typesetting,
													remaining essentially
													unchanged. It was
													popularised in the 1960s
													with the release of Letraset
													sheets containing Lorem
													Ipsum passages, and more
													recently with desktop
													publishing software like
													Aldus PageMaker including
													versions of Lorem Ipsum.
												</p></b-card-text
											>
										</b-card-body>
									</b-collapse>
								</b-card>
							</div>
							<h3>Sales Questions</h3>
							<div class="accordion" role="tablist">
								<b-card no-body>
									<b-card-header
										header-tag="header"
										role="tab"
									>
										<b-button
											block
											v-b-toggle.sales1
											variant="info"
											>Do I need to make a
											payment?</b-button
										>
									</b-card-header>
									<b-collapse
										id="sales1"
										visible
										accordion="my-accordion"
										role="tabpanel"
									>
										<b-card-body>
											<b-card-text
												><p>
													Lorem Ipsum is simply dummy
													text of the printing and
													typesetting industry. Lorem
													Ipsum has been the
													industry's standard dummy
													text ever since the 1500s,
													when an unknown printer took
													a galley of type and
													scrambled it to make a type
													specimen book. It has
													survived not only five
													centuries, but also the leap
													into electronic typesetting,
													remaining essentially
													unchanged. It was
													popularised in the 1960s
													with the release of Letraset
													sheets containing Lorem
													Ipsum passages, and more
													recently with desktop
													publishing software like
													Aldus PageMaker including
													versions of Lorem Ipsum.
												</p></b-card-text
											>
										</b-card-body>
									</b-collapse>
								</b-card>
								<b-card no-body>
									<b-card-header
										header-tag="header"
										role="tab"
									>
										<b-button
											block
											v-b-toggle.sales2
											variant="info"
											>Do I need to make a
											payment?</b-button
										>
									</b-card-header>
									<b-collapse
										id="sales2"
										visible
										accordion="my-accordion"
										role="tabpanel"
									>
										<b-card-body>
											<b-card-text
												><p>
													Lorem Ipsum is simply dummy
													text of the printing and
													typesetting industry. Lorem
													Ipsum has been the
													industry's standard dummy
													text ever since the 1500s,
													when an unknown printer took
													a galley of type and
													scrambled it to make a type
													specimen book. It has
													survived not only five
													centuries, but also the leap
													into electronic typesetting,
													remaining essentially
													unchanged. It was
													popularised in the 1960s
													with the release of Letraset
													sheets containing Lorem
													Ipsum passages, and more
													recently with desktop
													publishing software like
													Aldus PageMaker including
													versions of Lorem Ipsum.
												</p></b-card-text
											>
										</b-card-body>
									</b-collapse>
								</b-card>
								<b-card no-body>
									<b-card-header
										header-tag="header"
										role="tab"
									>
										<b-button
											block
											v-b-toggle.sales3
											variant="info"
											>Do I need to make a
											payment?</b-button
										>
									</b-card-header>
									<b-collapse
										id="sales3"
										visible
										accordion="my-accordion"
										role="tabpanel"
									>
										<b-card-body>
											<b-card-text
												><p>
													Lorem Ipsum is simply dummy
													text of the printing and
													typesetting industry. Lorem
													Ipsum has been the
													industry's standard dummy
													text ever since the 1500s,
													when an unknown printer took
													a galley of type and
													scrambled it to make a type
													specimen book. It has
													survived not only five
													centuries, but also the leap
													into electronic typesetting,
													remaining essentially
													unchanged. It was
													popularised in the 1960s
													with the release of Letraset
													sheets containing Lorem
													Ipsum passages, and more
													recently with desktop
													publishing software like
													Aldus PageMaker including
													versions of Lorem Ipsum.
												</p></b-card-text
											>
										</b-card-body>
									</b-collapse>
								</b-card>
							</div>
							<h3>Usage Guide</h3>
							<div class="accordion" role="tablist">
								<b-card no-body>
									<b-card-header
										header-tag="header"
										role="tab"
									>
										<b-button
											block
											v-b-toggle.guide1
											variant="info"
											>Do I need to make a
											payment?</b-button
										>
									</b-card-header>
									<b-collapse
										id="guide1"
										visible
										accordion="my-accordion"
										role="tabpanel"
									>
										<b-card-body>
											<b-card-text
												><p>
													Lorem Ipsum is simply dummy
													text of the printing and
													typesetting industry. Lorem
													Ipsum has been the
													industry's standard dummy
													text ever since the 1500s,
													when an unknown printer took
													a galley of type and
													scrambled it to make a type
													specimen book. It has
													survived not only five
													centuries, but also the leap
													into electronic typesetting,
													remaining essentially
													unchanged. It was
													popularised in the 1960s
													with the release of Letraset
													sheets containing Lorem
													Ipsum passages, and more
													recently with desktop
													publishing software like
													Aldus PageMaker including
													versions of Lorem Ipsum.
												</p></b-card-text
											>
										</b-card-body>
									</b-collapse>
								</b-card>
								<b-card no-body>
									<b-card-header
										header-tag="header"
										role="tab"
									>
										<b-button
											block
											v-b-toggle.guide2
											variant="info"
											>Do I need to make a
											payment?</b-button
										>
									</b-card-header>
									<b-collapse
										id="guide2"
										visible
										accordion="my-accordion"
										role="tabpanel"
									>
										<b-card-body>
											<b-card-text
												><p>
													Lorem Ipsum is simply dummy
													text of the printing and
													typesetting industry. Lorem
													Ipsum has been the
													industry's standard dummy
													text ever since the 1500s,
													when an unknown printer took
													a galley of type and
													scrambled it to make a type
													specimen book. It has
													survived not only five
													centuries, but also the leap
													into electronic typesetting,
													remaining essentially
													unchanged. It was
													popularised in the 1960s
													with the release of Letraset
													sheets containing Lorem
													Ipsum passages, and more
													recently with desktop
													publishing software like
													Aldus PageMaker including
													versions of Lorem Ipsum.
												</p></b-card-text
											>
										</b-card-body>
									</b-collapse>
								</b-card>
								<b-card no-body>
									<b-card-header
										header-tag="header"
										role="tab"
									>
										<b-button
											block
											v-b-toggle.guide3
											variant="info"
											>Do I need to make a
											payment?</b-button
										>
									</b-card-header>
									<b-collapse
										id="guide3"
										visible
										accordion="my-accordion"
										role="tabpanel"
									>
										<b-card-body>
											<b-card-text
												><p>
													Lorem Ipsum is simply dummy
													text of the printing and
													typesetting industry. Lorem
													Ipsum has been the
													industry's standard dummy
													text ever since the 1500s,
													when an unknown printer took
													a galley of type and
													scrambled it to make a type
													specimen book. It has
													survived not only five
													centuries, but also the leap
													into electronic typesetting,
													remaining essentially
													unchanged. It was
													popularised in the 1960s
													with the release of Letraset
													sheets containing Lorem
													Ipsum passages, and more
													recently with desktop
													publishing software like
													Aldus PageMaker including
													versions of Lorem Ipsum.
												</p></b-card-text
											>
										</b-card-body>
									</b-collapse>
								</b-card>
							</div>
						</div>
					</b-tab>
					<b-tab title="Pricing & Plans">2</b-tab>
					<b-tab title="Sales Questions">3</b-tab>
					<b-tab title="Usage Guide">4</b-tab>
				</b-tabs>
			</div>
			<h4>No answers to your query?</h4>
			<p class="query">
				If you cannot find answer to your question in our Help Center
				you can always contact us. We will answer to you shortly!
			</p>
			<div class="row query__boxes">
				<div class="col-sm-6">
					<div class="contentBox">
						<p>Send us email</p>
						<p>We will answer to you shortly!</p>
						<a href="#" class="btn btn-default">Send us email</a>
					</div>
				</div>
				<div class="col-sm-6">
					<div class="contentBox">
						<p>Chat with us</p>
						<p>We’re available online 24/7!</p>
						<a href="#" class="btn btn-default">Chat with us</a>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>
<script>
import BaseBreadCrumb from '@/common/components/base/BaseBreadCrumb.vue';
import { helpCenterBreadCrumbs } from "@/common/constant/breadCrumbs"

export default {
	components: {
		BaseBreadCrumb,
	},

	data() {
		return {
			breadCrumbsItems: [...helpCenterBreadCrumbs],
		};
	},
};
</script>

<style lang="scss" scoped>
.helpCenter {
	.form-group {
		input {
			background: #f5f5f5;
			padding-left: rem(56px);
			font-weight: 400;
			background-image: url("data:image/svg+xml,%3Csvg width='24' height='24' viewBox='0 0 24 24' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath fill-rule='evenodd' clip-rule='evenodd' d='M11 3C6.58172 3 3 6.58172 3 11C3 15.4183 6.58172 19 11 19C15.4183 19 19 15.4183 19 11C19 6.58172 15.4183 3 11 3ZM11 5C14.3137 5 17 7.68629 17 11C17 14.3137 14.3137 17 11 17C7.68629 17 5 14.3137 5 11C5 7.68629 7.68629 5 11 5Z' fill='%238E8E8E'/%3E%3Cg opacity='0.5'%3E%3Cpath fill-rule='evenodd' clip-rule='evenodd' d='M15.2926 15.2971C15.6529 14.9365 16.2201 14.9085 16.6125 15.2133L16.7068 15.2965L20.7068 19.2928C21.0975 19.6832 21.0978 20.3164 20.7074 20.7071C20.3471 21.0677 19.7799 21.0957 19.3875 20.7908L19.2932 20.7077L15.2932 16.7113C14.9025 16.321 14.9022 15.6878 15.2926 15.2971Z' fill='%238E8E8E'/%3E%3C/g%3E%3C/svg%3E%0A");
			background-repeat: no-repeat;
			background-position: rem(25px) center;
			max-height: 64px;
			@media screen and (max-width:767px){
				max-height:50px;
				padding-left:rem(40px);
				background-position: 5px center;
			}
		}
	}
	::v-deep .tabs {
		.nav-pills {
			@media screen and (max-width: 767px) {
				// justify-content: center;
			}
			li {
				@media screen and (max-width: 767px) {
					margin-bottom: 15px;
				}
			}
		}
		.tab-content {
			margin-top: rem(48px);
			@media screen and (max-width:767px){
				margin-top:rem(35px);
			}

			h3 {
				font-size: rem(24px);
				margin-top: rem(48px);
				margin-bottom: 0;
				@media screen and (max-width:767px){
					font-size:rem(20px);
					margin-top:rem(35px);
				}
			}
			.accordion {
				margin-top: rem(10px);
				.card {
					border: 0;
					border-bottom: 1px solid var(--borderColor);
					border-radius: 0;
					padding: 0;
					margin-bottom: 0;
					> .card-header {
						background: transparent;
						border: 0;
						padding: 0;
						.btn {
							background: transparent;
							font-weight: 400;
							font-size: rem(16px);
							color: #171716;
							position: relative;
							width: 100%;
							text-align: left;
							padding: rem(27px);
							border: none;
							border-radius: 0;
							height: auto;
							justify-content: space-between;
							&::before {
								position: absolute;
								content: '';
								left: 0;
								top: 50%;
								transform: translateY(-50%);
								height: 7px;
								width: 7px;
								background: var(--default);
								border-radius: 50%;
							}
							
							&:after {
								content: '';
								position: absolute;
								width: 24px;
								height: 24px;
								background-image: url("data:image/svg+xml,%3Csvg width='24' height='24' viewBox='0 0 24 24' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath fill-rule='evenodd' clip-rule='evenodd' d='M4.80342 11.0078C4.31035 11.0695 3.92886 11.4902 3.92886 12C3.92886 12.5523 4.37658 13 4.92886 13L10.9999 13L10.9999 19.0711L11.0077 19.1965C11.0694 19.6896 11.4901 20.0711 11.9999 20.0711C12.5522 20.0711 12.9999 19.6234 12.9999 19.0711L12.9999 13H19.071L19.1964 12.9922C19.6895 12.9305 20.071 12.5098 20.071 12C20.071 11.4477 19.6233 11 19.071 11H12.9999L12.9999 4.92893L12.9921 4.80349C12.9304 4.31042 12.5097 3.92893 11.9999 3.92893C11.4476 3.92893 10.9999 4.37665 10.9999 4.92893L10.9999 11L4.92886 11L4.80342 11.0078Z' fill='%23C9C9C9'/%3E%3C/svg%3E%0A");
								background-repeat: no-repeat;
								right: 32px;
								top: 50%;
								transform: translateY(-50%);
								@media screen and (max-width: 767px) {
									right: 0;
								}
							}
							@media screen and (max-width: 767px) {
								padding: rem(20px);
								&:after{
									transform: scale(.9) translateY(-50%);
								}
							}
							&.not-collapsed {
								&:after {
									top: 63%;
									background-image: url("data:image/svg+xml,%3Csvg width='18' height='2' viewBox='0 0 18 2' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M0.928862 1C0.928862 0.490199 1.31035 0.069498 1.80342 0.00779145L1.92886 -7.91831e-09L16.071 2.8711e-07C16.6233 2.8711e-07 17.071 0.447716 17.071 1C17.071 1.5098 16.6895 1.9305 16.1964 1.99221L16.071 2L1.92886 2C1.37658 2 0.928862 1.55228 0.928862 1Z' fill='%23C9C9C9'/%3E%3C/svg%3E%0A");
								}
							}
							&:focus {
								outline: unset;
							}
						}
					}
					.card-body {
						padding: 0;
						padding-top: rem(5px);

						p {
							font-size: rem(16px);
							color: var(--default);
						}
					}
				}
			}
		}
	}
	h4 {
		font-size: rem(28px);
		margin-top: rem(48px);
		@media screen and (max-width:767px){
			font-size:rem(23px);
			margin-top:rem(25px);
		}
	}
	.query {
		font-size: rem(14px);
	}
	.contentBox {
		padding: rem(32px);
		background: #f5f5f5;
		border: 0;
		@media screen and (max-width: 575px) {
			margin-bottom: rem(20px);
			text-align: center;
			border: 0;
			padding-bottom: rem(20px);
		}
		p {
			font-size: rem(20px);
			font-weight: 500;
			color: var(--textPrimary);
			margin-bottom: rem(8px);
		}
		p:nth-child(2) {
			font-size: rem(14px);
			font-weight: 400;
			color: var(--default);
			margin-bottom: rem(16px);
		}
		a {
			padding-left: rem(48px);
			padding-right: rem(48px);
			@media screen and (max-width:767px){
				padding:rem(10px) rem(35px);
				height:40px;
			}
		}
	}
}
</style>
