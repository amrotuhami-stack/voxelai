<template>
	<div class="home">
		<h4>Distributor</h4>
		<ul>
			<li>
				<a href="/distributors/dashboard">Dashboard</a>
			</li>
			<li>
				<a href="/distributors/my-patient">My Patient</a>
			</li>
			<li>
				<a href="/distributors/doctor-orders">Doctor Orders</a>
			</li>
			<li>
				<a href="/distributors/orders">Orders</a>
			</li>
			<li>
				<a href="/distributors/checkout">Checkout</a>
			</li>
			<li>
				<a href="/distributors/account-settings">Account Settings</a>
			</li>
			<li>
				<a href="/distributors/checkout-payment-complete"
					>Checkout Payment complete</a
				>
			</li>
			<li>
				<a href="/distributors/help-center">Help Center</a>
			</li>
		</ul>
		<h4>Shoping Cart</h4>
		<ul>
			<li>
				<a href="/shopping-cart">shoping carts</a>
			</li>
			<li>
				<a href="/empty-shopping-cart">empty-shopping-cart</a>
			</li>
		</ul>
		<h4>DB - checkout</h4>
		<ul>
			<li>
				<a href="/checkout">checkOut</a>
			</li>
			<li>
				<a href="/checkout-payment-complete"
					>checkout-payment-complete</a
				>
			</li>
		</ul>
		<h4>DB - Existing services</h4>
		<ul>
			<li>
				<a href="/start-service-existing">start-service-existing</a>
			</li>
		</ul>
		<h4>Shipping</h4>
		<ul>
			<li>
				<a href="/new-service-flow-shipment"
					>new-service-flow-shipment</a
				>
			</li>
		</ul>
		<h4>DB - Service Details</h4>
		<ul>
			<li>
				<a href="/new-service-flow">new-service-flow</a>
			</li>
		</ul>
		<h4>DB - Start New Service</h4>
		<ul>
			<li>
				<a href="/service">service</a>
			</li>
		</ul>
		<h4>DB - Account Settings</h4>
		<ul>
			<li>
				<a href="/account-settings">Account Settings</a>
			</li>
		</ul>
		<h4>DB - My orders</h4>
		<ul>
			<li>
				<a href="/my-order">my-order</a>
			</li>
		</ul>
		<h4>DB - My patients</h4>
		<ul>
			<li>
				<a href="/my-patients">my-patients</a>
			</li>
			<li>
				<a href="patient-service">patient-service</a>
			</li>
		</ul>
		<h4>DB - Deals and Offers</h4>
		<ul>
			<li>
				<a href="/deals-and-offers">deals-and-offers</a>
			</li>
		</ul>
		<h4>DB - Help Center</h4>
		<ul>
			<li>
				<a href="/help-center">help-center</a>
			</li>
		</ul>
		<h4>DashBoard</h4>
		<ul>
			<li>
				<a href="/dashboard">dashboard</a>
			</li>
			<li>
				<a href="/server-down">server-down</a>
			</li>
		</ul>
		<h4>DB - shop</h4>
		<ul>
			<li>
				<a href="/shop">shop</a>
			</li>
			<li>
				<a href="/product-details">product-details</a>
			</li>
		</ul>
		<h4>DB - Create Your Own Analysis</h4>
		<ul>
			<li>
				<a href="/start-new-ceph-service">start-new-ceph-service</a>
			</li>
			<!-- <li>
				<a href="/start-ceph-service-analysis"
					>start-ceph-service-analysis</a
				>
			</li>
			<li>
				<a href="/start-new-ceph-service-patient-record"
					>start-new-ceph-service-patient-record</a
				>
			</li> -->
		</ul>
		<h4>DB - Create Your Own Analysis</h4>
		<ul>
			<li>
				<a href="/start-new-ceph-service-payment-complete"
					>start-new-ceph-service-payment-complete</a
				>
			</li>
			<li>
				<a href="/start-ceph-service-analysis"
					>start-ceph-service-analysis</a
				>
			</li>
			<li>
				<a href="/start-ceph-service-patient-record"
					>start-new-ceph-service-patient-record</a
				>
			</li>
		</ul>
	</div>
</template>

<script>
// @ is an alias to /src

export default {
	name: 'Home',
};
</script>
<style lang="scss" scoped>
ul {
	list-style: none;
	li {
		margin-bottom: rem(5px);
	}
}
</style>
