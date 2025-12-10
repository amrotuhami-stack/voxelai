<template>
	<div
		class="baseSliderWrapper"
		:class="navigationLayout == 'side' ? 'sideWrapper' : ''"
	>
		<div
			class="swiper-container"
			:id="sliderId"
			ref="slider"
			role="region"
			aria-label="carousel"
			:aria-live="this.isPause ? 'polite' : 'off'"
		>
			<div class="swiper-wrapper">
				<slot></slot>
			</div>
		</div>
		<div
			:id="`sliderNavigation_${this.sliderId}`"
			:class="[
				'sliderNavigation',
				this.totalSlides == 1 ? 'singleSlide' : '',
				navigationLayout == 'side'
					? 'sideNavigation'
					: navigationLayout == 'bottom'
					? 'bottomNavigation'
					: '',
				navigationTheme == 'simple' ? 'navigationSimple' : '',
				this.carouselSettings.thumbs ? '' : '',
			]"
		>
			<div class="container-fluid">
				<div class="sliderNavigation__controls">
					<button
						type="button"
						id="prevArrow"
						role="button"
						aria-label="Previous"
						class="sliderNavigation__controls--arrow"
						:class="[
							'sliderNavigation__controls--prev' + this.sliderId,
							totalSlides == 1 ? 'd-none' : '',
						]"
					>
						<svg
							width="8"
							height="14"
							viewBox="0 0 8 14"
							fill="currentColor"
							xmlns="http://www.w3.org/2000/svg"
						>
							<path
								fill-rule="evenodd"
								clip-rule="evenodd"
								d="M0.390524 13.2755C-0.090121 12.7948 -0.127094 12.0385 0.279606 11.5155L0.390524 11.3899L4.78 6.99935L0.390524 2.60882C-0.0901215 2.12818 -0.127094 1.37187 0.279606 0.848817L0.390524 0.723207C0.871169 0.242562 1.62748 0.205589 2.15053 0.612288L2.27614 0.723207L7.60947 6.05654C8.09012 6.53719 8.12709 7.29349 7.72039 7.81655L7.60947 7.94216L2.27614 13.2755C1.75544 13.7962 0.911223 13.7962 0.390524 13.2755Z"
								fill="currentColor"
							/>
						</svg>
						<!-- <span class="sr-only">Previous Slide</span> -->
					</button>
					<button
						type="button"
						role="button"
						id="nextArrow"
						aria-label="Next"
						class="sliderNavigation__controls--arrow"
						:class="[
							'sliderNavigation__controls--next' + this.sliderId,
							totalSlides == 1 ? 'd-none' : '',
						]"
					>
						<svg
							width="8"
							height="14"
							viewBox="0 0 8 14"
							fill="currentColor"
							xmlns="http://www.w3.org/2000/svg"
						>
							<path
								fill-rule="evenodd"
								clip-rule="evenodd"
								d="M0.390524 13.2755C-0.090121 12.7948 -0.127094 12.0385 0.279606 11.5155L0.390524 11.3899L4.78 6.99935L0.390524 2.60882C-0.0901215 2.12818 -0.127094 1.37187 0.279606 0.848817L0.390524 0.723207C0.871169 0.242562 1.62748 0.205589 2.15053 0.612288L2.27614 0.723207L7.60947 6.05654C8.09012 6.53719 8.12709 7.29349 7.72039 7.81655L7.60947 7.94216L2.27614 13.2755C1.75544 13.7962 0.911223 13.7962 0.390524 13.2755Z"
								fill="currentColor"
							/>
						</svg>
					</button>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import Swiper from 'swiper/bundle';
import 'swiper/swiper-bundle.css';
export default {
	props: {
		carouselSettings: Object,
		carouselId: {
			type: String,
			default: '',
		},
		navigationLayout: String,
		navigationTheme: String,
		fractionPagination: {
			default: false,
			type: Boolean,
		},
		fractionPaginationActive: {
			default: false,
			type: Boolean,
		},
		controller: Object,
		sliderType: {
			type: String,
			default: 'carousel',
		},
	},
	data() {
		return {
			totalSlides: 0,
			currentSlide: 0,
			isPause: true,
			sliderId: 'slider-' + this.randomNumber(),
			slider: Object,
			swiper: Object,
			sliderObj: null,
		};
	},
	created() {
		if (this.carouselId != '') {
			this.sliderId = this.carouselId;
		}
	},
	mounted() {
		this.setUpCarousel();
	},
	methods: {
		setUpCarousel: function () {
			var navigation = {
				nextEl: '.sliderNavigation__controls--next' + this.sliderId,
				prevEl: '.sliderNavigation__controls--prev' + this.sliderId,
			};
			var pagination = {
				el: '.swiper-pagination' + this.sliderId,
				type: 'fraction',
			};
			var keyboard = { enabled: false };
			var draggable = { draggable: false };
			var swipping = { noSwiping: false };
			this.carouselSettings.navigation = navigation;
			if (!this.carouselSettings.keyboard) {
				this.carouselSettings.keyboard = keyboard;
			}
			this.carouselSettings.pagination = pagination;
			this.carouselSettings.draggable = draggable;
			this.carouselSettings.noSwiping = false;
			//this.carouselSettings.simulateTouch = false
			//this.carouselSettings.touchRatio = 0
			this.slider = document.getElementById(this.sliderId);
			if (this.carouselSettings.autoplay) {
				this.isPause = false;
			}
			if (this.slider) {
				this.swiper = new Swiper(this.slider, this.carouselSettings);
				var length = this.swiper.slides.length;
				if (length == 0) {
					length =
						this.slider.querySelectorAll('.swiper-slide').length;
					document
						.querySelector('#sliderNavigation_' + this.sliderId)
						.classList.add('d-none');
				}
				length == 1
					? document
							.querySelector('#sliderNavigation_' + this.sliderId)
							.classList.add('d-none')
					: '';
				this.totalSlides = length;
			}
			this.currentSlide = this.swiper.activeIndex + 1;
			this.$emit('init', this.swiper);
			this.accessibility();
			this.mainBanner();
		},
		accessibility: function () {
			var slide = this.slider.querySelectorAll('.swiper-slide');
			if (!this.isPause) {
				this.slider.setAttribute('aria-live', 'off');
			}
			if (this.sliderType == 'slider') {
				slide.forEach((element) => {
					element.setAttribute('aria-hidden', 'true');
					element.setAttribute('tabindex', '-1');
				});
				setTimeout(() => {
					this.slider
						.querySelector('.swiper-slide-active')
						.setAttribute('aria-hidden', 'false');
					this.slider
						.querySelector('.swiper-slide-active')
						.setAttribute('tabindex', 0);
				}, 400);
				this.swiper.on('slideChangeTransitionEnd', (swiper) => {
					this.currentSlide = swiper.activeIndex;
					slide.forEach((element) => {
						element.setAttribute('tabindex', '-1');
						element.setAttribute('aria-hidden', 'true');
					});
					setTimeout(() => {
						this.slider
							.querySelector('.swiper-slide-active')
							.setAttribute('tabindex', '0');
						this.slider
							.querySelector('.swiper-slide-active')
							.setAttribute('aria-hidden', 'false');
						// slider.querySelector(".swiper-slide-active").focus();
					}, 1000);
				});
			}
		},
		mainBanner: function () {
			this.swiper.on('slideChange', (e) => {
				this.currentSlide = e.activeIndex + 1;
				setTimeout(() => {
					//if (this.sliderId == 'mainBanner') {
					var currentSlide = this.slider.querySelector(
						'.swiper-slide-active'
					);
					var mp4 = currentSlide.querySelector('.video-mp4');
					var image = currentSlide.querySelector(
						'.banner__slide--image'
					);
					var youtube = currentSlide.querySelector('.video-youtube');
					if (currentSlide.classList.contains('has-video')) {
						if (mp4) {
							var video = mp4.querySelector('video');
							video.setAttribute('tabindex', 0);
							video.play();
							image.classList.add('invisible');
							this.stopYoutube();
						} else if (youtube) {
							var vs = youtube.dataset.src;
							youtube
								.querySelector('iframe')
								.setAttribute('src', vs);
							youtube
								.querySelector('iframe')
								.setAttribute('tabindex', -1);
							image.classList.add('invisible');
							this.stopMp4();
						} else {
							this.stopYoutube();
							this.mp4();

							image.classList.remove('invisible');
						}
					}
					//}
				}, 500);
			});
		},
		stopYoutube: function () {
			var iframes = this.slider.querySelectorAll('iframe');
			iframes.forEach((element) => {
				element.setAttribute('src', '');
				element.setAttribute('tabindex', -1);
			});
		},
		stopMp4: function () {
			var mp4 = this.slider.querySelectorAll('video');
			mp4.forEach((element) => {
				element.pause();
				element.setAttribute('tabindex', -1);
			});
		},
		pausePlay: function () {
			if (this.isPause) {
				this.swiper.autoplay.start();
				this.isPause = false;
			} else {
				this.swiper.autoplay.stop();
				this.isPause = true;
			}
		},
		randomNumber: function () {
			return Math.floor(Math.random() * (100000 - 1 + 1) + 1);
		},
	},
};
</script>

<style lang="scss" scoped>
.sliderNavigation {
	position: absolute;
	top: -10px;
	width: 100%;
	--color: #fff;
	--arrow: #6b6b6b;
	--border: #6b6b6b;
	--pause: #fff;
	--topborder: #fff;
	color: var(--color);
	z-index: 1;
	right: 0;
	button {
		background: transparent;
		border: 0;
	}
	&__controls {
		@include flex(center, space-between);
		max-width: 130px;
		margin: 0 0 0 auto;
		@media screen and (max-width: 991px) {
			max-width: 220px;
			justify-content: space-around;
		}
		::v-deep svg {
			height: 18px;
			width: 18px;
			color: #6b6b6b;
			// @media screen and (max-width: 991px) {
			//     transform: scale(0.8);
			//     transform-origin: center;
			// }
		}
		&--arrow {
			width: rem(52px);
			height: rem(52px);
			border: solid 1px var(--border) !important;
			border-radius: 50%;
			color: var(--arrow);

			@include flex(center, center);
			@media screen and (max-width: 991px) {
				width: 45px;
				height: 45px;
			}
			@media screen and (min-width: 1199px) {
				&:hover {
					background: #6b6b6b !important;
					color: #fff;
					::v-deep {
						svg {
							color: #fff;
						}
					}
				}
			}
			&.swiper-button-disabled {
				pointer-events: none;
				opacity: 0.5;
			}
			&#prevArrow {
				::v-deep {
					svg {
						transform: rotate(180deg);
					}
				}
			}
		}
	}
	&.singleSlide {
		display: none;
	}
}
</style>
