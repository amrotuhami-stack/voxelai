<template>
	<div>
		<!--<div class="patientType">
			<div class="inner-title">
				Select your patient type 
				<svg-icon
					icon-id="info-circle"
					icon-viewbox="0 0 24 24"
				></svg-icon>
			</div>
			<div class="row" v-if="product && caseDefinition">
				<div class="col-md-4 col-sm-6" :class="item.children.length > 0 ? 'show-content' : ''" v-for='item in caseDefinition.children' :key="item.id" @click="updatePatientType(item.slug)">
					<div class="contentBox" >
						<div class="image">
							<img :src="item.image" :alt="item.slug" class="img-fluid"/>
						</div>
						<h4>
							{{item.title}}
						</h4>
						<div>
							{{item.Descrption}}
						</div>
					</div>
				</div>
			</div>
			<div class="CaseList">
				<div class="CaseList--card" :class="item.show" v-for='item in caseList' :key="item.index">
					<div class="contentBox">
						<div>
							<div class="image">
								<img :src="`${require(`@/assets/images/${item.image}`)}`" alt="" class="img-fluid"/>
							</div>
							<p>
								{{item.title}}<span>{{item.subTitle}}</span>
							</p>
							<span class="checked"></span>
						</div>
						
					</div>
				</div>
			</div> 
		</div>-->
	</div> 
</template>

<script>
import { mapGetters } from 'vuex';
import { SERVICE } from '@/store/modules/service/actions';

export default {
	props: {
		product: Object,
		updateService: Function,
		serviceData: Object,
		readOnly: {
      		type: Boolean,
      		default: false,
    	},
	},
	data(){
		return{
			selectedPatientTypeSlug: null,
			caseDefinition: null,
		}
	},
	created(){
		this.caseDefinition = this.product.case_definitions[0].case_definition.children.filter((item) => item.slug === this.serviceData.caseSlug)[0]
	},
	mounted() {
		let items = document.querySelectorAll('.patientType .contentBox');
		if(!this.readOnly) {
			items.forEach(item =>{
				item.addEventListener('click',()=>{
					items.forEach(i => i.classList.remove('active'))
					item.classList.add('active')
				})
			})
		}
	},
	methods: {
		updatePatientType(slug){
			if(!this.readOnly) {
				this.selectedPatientTypeSlug = slug;
			}
		},
	}
	
	
};
</script>

<style lang="scss" scoped>
.patientType {
	margin-top: rem(25px);
	display: none;
	.contentBox {
		padding: rem(16px);
		height: 100%;
		@media screen and (max-width: 991px) {
			margin-bottom: 15px;
			height: calc(100% - 15px);
		}
		.image {
			text-align: center;
			background: #F5F5F5;
			border-radius: 6px;
			min-height: 123px;
			display: flex;
			align-items: center;
			justify-content: center;
		}
		h4 {
			margin-top: rem(20px);
			margin-bottom: rem(12px);
			font-size: rem(16px);
		}
		ul {
			margin-left: rem(20px);
			list-style: disc;
			li {
				font-size: rem(14px);
				font-weight: 400;
				color: var(--default);
				line-height: 1.1;
				margin-bottom: rem(0px);
				&:not(:last-child) {
					margin-bottom: rem(12px);
				}
				&::marker {
					color: #a8d5ee;
					font-size: rem(20px);
				}
			}
		}
		&.active {
			border-color: var(--primary);
			.image {
				background: #EEF7FB;
			}
		}
	}
}
</style>
