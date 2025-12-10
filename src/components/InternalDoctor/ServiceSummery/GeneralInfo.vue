<template>
	<div>
		<div class="contentBox">
            <div class="row">
			    <div class="col-lg-6">
			    	<p>Patient Name</p>
                    <h6>{{ service.patient_obj.first_name + " " + service.patient_obj.last_name + ",  " +  Math.ceil(service.patient_obj.age, 0) + " years, "  + service.patient_obj.gender}}</h6>
			    </div>
                <div class="col-lg-6">
			    	<p>Doctor Name</p>
                    <h6>{{ service.owner_obj.name || service.owner_obj.first_name + " " + service.owner_obj.last_name }}</h6>
			    </div>
				<div class="divider"></div>
            </div>
			<div class="row">
			    <div class="col-lg-12">
			    	<p>Service Name</p>
                    <h6>{{service.order_line_obj.product_obj.title}}</h6>
			    </div>
            </div>
		</div>
	</div>
</template>

<script>

export default {
	props: {
		service: Object,
	},
	data() {
		return {
		};
	},
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
	.row {
        p {
            margin-bottom: rem(8px);
			font-size: 14px;
        }
		h6 {
			margin-bottom: rem(12px);
			text-transform: capitalize;
		}
		.divider {
			background-color: var(--borderColor);
			height: 00.5px;
			margin-top: rem(12px);
			margin-bottom: rem(24px);
		}
    }
}
</style>
