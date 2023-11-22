import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'
import MainView from '@/views/MainView.vue'
import SignUpView from '@/views/SignUpView.vue'
import LogInView from '@/views/LogInView.vue'
import ArticleView from '@/views/ArticleView.vue'
import ArticleCreateView from '@/views/ArticleCreateView.vue'
import ArticleDetailView from '@/views/ArticleDetailView.vue'
import ArticleUpdateView from '@/views/ArticleUpdateView.vue'
import MapView from '@/views/MapView.vue'
import ExchangeView from '@/views/ExchangeView.vue'
import FinanceComparsionView from '@/views/FinanceComparsionView.vue'
import DepositProductDetailView from '@/views/DepositProductDetailView.vue'
import SavingProductDetailView from '@/views/SavingProductDetailView.vue'
import ProfileView from '@/views/ProfileView.vue'
import UserUpdateView from '@/views/UserUpdateView.vue'
import PortfolioView from '@/views/PortfolioView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'main',
      component: MainView
    },
    {
      path: '/compare',
      name: 'compare',
      component: FinanceComparsionView
    },
    {
      path: '/deposit_product-detail/:fin_prdt_cd',
      name: 'deposit_product_detail',
      component: DepositProductDetailView
    },
    {
      path: '/saving_product-detail/:fin_prdt_cd',
      name: 'saving_product_detail',
      component: SavingProductDetailView
    },
    {
		path: '/signup',
		name: 'signup',
		component: SignUpView
		},
    {
		path: '/login',
		name: 'login',
		component: LogInView
		},
    {
		path: '/profile',
		name: 'profile',
		component: ProfileView
		},
    {
		path: '/protfolio',
		name: 'protfolio',
		component: PortfolioView
		},
    {
		path: '/update',
		name: 'update',
		component: UserUpdateView
		},
		{
			path: '/articles',
			name: 'articles',
			component: ArticleView
		},
    {
			path: '/article-create',
			name: 'article_create',
			component: ArticleCreateView
		},
    {
			path: '/article-detail/:article_id',
			name: 'article_detail',
			component: ArticleDetailView
		},
		{
			path: '/article-update/:article_id',
			name: 'article_update',
			component: ArticleUpdateView
		},
    {
		path: '/map',
		name: 'map',
		component: MapView
	},
    {
		path: '/exchange',
		name: 'exchange',
		component: ExchangeView
	},
  ]
})

// 메인페이지 로그인 상태로만 이용 가능
router.beforeEach((to, from) => {
  const userStore = useUserStore()
  if ((to.name === 'signup' || to.name === 'login') && (userStore.isLogin)) {
    window.alert('이미 로그인이 되어있습니다.')
    return { name: 'main' }
  }
  if ((to.name === 'exchange' || to.name === 'map') && (!userStore.isLogin)) {
    window.alert('로그인이 필요합니다.')
    return { name: 'main' }
  }
})
export default router
