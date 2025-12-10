<template>
	<div class="contentBox">
		<div class="serviceRow" v-for="(item, index) in service" :key="index">
			<div class="serviceRow__image" v-if="item.product_class == 'online-ai-service'">
				<img v-if="item && item.parent_obj.images.length > 0"
					:src="item.parent_obj.images[0].original"
					alt=""
					class="img-fluid"
				/>
			</div>
			<div class="serviceRow__image" v-if="item.product_class != 'online-ai-service'">
				<img v-if="item && item.images.length > 0"
					:src="item.images[0].original"
					alt=""
					class="img-fluid"
				/>
			</div>
			<div class="serviceRow__title">
				<span v-if="item.product_class == 'online-ai-service'">
					{{ item.parent_obj.title }} - {{ item.title }}
				</span>
				<span v-if="item.product_class != 'online-ai-service'">
					{{ item.title }}
				</span>
				<!-- <div class="serviceRow__cases" v-if="item.remaining">
					<div class="serviceRow__cases--progress">
						<b-progress
							:value="item.value"
							:max="item.max"
						></b-progress>
					</div>
					<div
						class="
							d-flex
							justify-content-between
							align-items-center
						"
					>
						<div class="serviceRow__cases--remaining">
							<span>{{ item.case }} </span
							>{{ item.remainingCase }}
							<svg-icon
								v-b-tooltip.hover
								title="cases remaining"
								icon-id="info-circle"
								icon-viewbox="0 0 24 24"
							></svg-icon>
						</div>
						<div class="serviceRow__cases--duration">
							{{ item.duration }}
						</div>
					</div>
				</div> -->
				<!-- <div class="serviceRow__details" v-if="item.seeMore">
					<a href="#" class="viewMore"
						>{{ item.detail }}
						<font-awesome-icon :icon="['fa', 'angle-right']"
					/></a>
				</div> -->
			</div>
			<!-- <div class="serviceRow__link">
				<a href="#" v-if="item.showBtn" class="btn btn-default">{{
					item.link
				}}</a>
			</div> -->
		</div>
	</div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
	props: {
		service: Array,
	},
	data() {
		return {
			value: 40,
			max: 100,
			services: [],
		};
	},
	// computed: {
	// 	...mapGetters(['orderLines']),
    // },
	// watch: {
	// 	orderLines(){
	// 		this.services = this.orderLines;
	// 	},
	// },
	mounted() {
		
	},
	methods: {
	}
};
</script>
