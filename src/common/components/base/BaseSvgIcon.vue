<template>
    
        <svg fill="currentColor" :viewBox="iconViewbox" :alt="iconAlt">
            <use :xlink:href="`#${iconId}`"></use>
        </svg>
    
</template>

<script>
export default {
    props: {
        iconId: String,
        iconViewbox: String,
        iconAlt: String,
    },
}
</script>

<style lang="scss" scoped></style>
