<template>
  <div class="users-list">
    <div v-if="users.length === 0" class="empty">
      <p>Nenhum usuário encontrado</p>
    </div>
    
    <div v-else>
      <UserCard 
        v-for="user in users" 
        :key="user.id"
        :user="user"
        :current-user-id="currentUserId"
        @edit="$emit('edit', $event)"
        @delete="$emit('delete', $event)"
      />
    </div>
  </div>
</template>

<script>
import UserCard from './UserCard.vue'

export default {
  name: 'UsersList',
  components: {
    UserCard
  },
  props: {
    users: {
      type: Array,
      required: true
    },
    currentUserId: {
      type: [String, Number],
      default: null
    }
  },
  emits: ['edit', 'delete']
}
</script>

<style scoped>
.users-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.empty {
  text-align: center;
  padding: 2rem;
  color: #666;
  background-color: #f8f9fa;
  border-radius: 10px;
}
</style>
