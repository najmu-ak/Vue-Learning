<template>
  <LayoutHeader>
    <template #left-header>
      <Breadcrumbs :items="[{ label: 'Students', route: { name: 'Students' } }]" />
    </template>
    <template #right-header>
      <Button variant="solid" :label="__('Add Student')" iconLeft="plus" @click="showCreateModal = true" />
    </template>
  </LayoutHeader>

  <div class="flex flex-col overflow-hidden">
    <div class="flex-1 overflow-y-auto">
      <div v-if="students.loading" class="flex items-center justify-center h-64">
        <Spinner size="lg" />
      </div>

      <div v-else-if="studentsList.length === 0" class="flex flex-col items-center justify-center h-64 text-gray-500">
        <ContactsIcon class="w-16 h-16 mb-4" />
        <p class="text-lg">No students found</p>
        <p class="text-sm">Click "Add Student" to create your first student</p>
      </div>

      <div v-else class="p-4">
        <div class="overflow-x-auto">
          <table class="w-full border-collapse">
            <thead>
              <tr class="border-b bg-gray-50">
                <th class="text-left p-3">ID</th>
                <th class="text-left p-3">Name</th>
                <th class="text-left p-3">Email</th>
                <th class="text-left p-3">Phone</th>
                <th class="text-left p-3">Course</th>
                <th class="text-left p-3">Teacher</th>
                <th class="text-left p-3">Organization</th>
                <th class="text-left p-3">Status</th>
                <th class="text-left p-3">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="student in studentsList" :key="student.name" class="border-b hover:bg-gray-50">
                <td class="p-3">{{ student.name }}</td>
                <td class="p-3">{{ student.student_name }}</td>
                <td class="p-3">{{ student.email }}</td>
                <td class="p-3">{{ student.phone || '-' }}</td>
                <td class="p-3">{{ student.course || '-' }}</td>
                <td class="p-3">{{ student.teacher || '-' }}</td>
                <td class="p-3">{{ student.organization || '-' }}</td>
                <td class="p-3">
                  <Badge :variant="student.status === 'Active' ? 'subtle' : 'gray'" :label="student.status" />
                </td>
                <td class="p-3">
                  <div class="flex gap-2">
                    <Button variant="ghost" size="sm" :label="__('Edit')" @click="editStudent(student)" />
                    <Button variant="ghost" size="sm" :label="__('Delete')" theme="red"
                      @click="deleteStudent(student)" />
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>

  <Dialog v-model="showCreateModal" :options="{ title: 'Create New Student', size: 'md' }">
    <template #body-content>
      <div class="space-y-4">
        <FormControl v-model="createFormData.student_name" :label="__('Student Name')" placeholder="Enter student name"
          required />
        <FormControl v-model="createFormData.email" :label="__('Email')" type="email" placeholder="student@example.com"
          required />
        <FormControl v-model="createFormData.phone" :label="__('Phone')" placeholder="+1234567890" />
        <FormControl v-model="createFormData.course" :label="__('Course')" placeholder="Enter course name" />
        
        <!-- Link Field for Teacher -->
        <div class="space-y-1.5">
          <label class="block text-sm text-gray-700">{{ __('Teacher') }}</label>
          <Link 
            v-model="createFormData.teacher"
            doctype="User"
            :placeholder="__('Select Teacher')"
          />
        </div>
        
        <!-- Link Field for Organization -->
        <div class="space-y-1.5">
          <label class="block text-sm text-gray-700">{{ __('Organization') }}</label>
          <Link 
            v-model="createFormData.organization"
            doctype="CRM Organization"
            :placeholder="__('Select Organization')"
          />
        </div>
        
        <FormControl v-model="createFormData.status" :label="__('Status')" type="select" :options="[
          { label: 'Active', value: 'Active' },
          { label: 'Inactive', value: 'Inactive' },
          { label: 'Graduated', value: 'Graduated' },
          { label: 'Dropped', value: 'Dropped' }
        ]" />
      </div>
    </template>
    <template #actions>
      <div class="flex gap-2 justify-end">
        <Button variant="solid" :label="__('Cancel')" @click="closeCreateModal" />
        <Button variant="solid" theme="primary" :label="__('Create')" :loading="creating" @click="createStudent" />
      </div>
    </template>
  </Dialog>

  <!-- Edit Modal -->
  <Dialog v-model="showEditModal" :options="{ title: 'Edit Student', size: 'md' }">
    <template #body-content>
      <div class="space-y-4">
        <FormControl v-model="editFormData.student_name" :label="__('Student Name')" placeholder="Enter student name"
          required />
        <FormControl v-model="editFormData.email" :label="__('Email')" type="email" placeholder="student@example.com"
          required />
        <FormControl v-model="editFormData.phone" :label="__('Phone')" placeholder="+1234567890" />
        <FormControl v-model="editFormData.course" :label="__('Course')" placeholder="Enter course name" />
        
        <!-- Link Field for Teacher -->
        <div class="space-y-1.5">
          <label class="block text-sm text-gray-700">{{ __('Teacher') }}</label>
          <Link 
            v-model="editFormData.teacher"
            doctype="User"
            :placeholder="__('Select Teacher')"
          />
        </div>
        
        <!-- Link Field for Organization -->
        <div class="space-y-1.5">
          <label class="block text-sm text-gray-700">{{ __('Organization') }}</label>
          <Link 
            v-model="editFormData.organization"
            doctype="CRM Organization"
            :placeholder="__('Select Organization')"
          />
        </div>
        
        <FormControl v-model="editFormData.status" :label="__('Status')" type="select" :options="[
          { label: 'Active', value: 'Active' },
          { label: 'Inactive', value: 'Inactive' },
          { label: 'Graduated', value: 'Graduated' },
          { label: 'Dropped', value: 'Dropped' }
        ]" />
      </div>
    </template>
    <template #actions>
      <Button variant="solid" :label="__('Cancel')" @click="closeEditModal" />
      <Button variant="solid" theme="primary" :label="__('Update')" :loading="updating" @click="updateStudent" />
    </template>
  </Dialog>

  <!-- Delete Confirmation -->
  <Dialog v-model="showDeleteModal" :options="{ title: 'Delete Student', size: 'sm' }">
    <template #body-content>
      <p>Are you sure you want to delete this student?</p>
    </template>
    <template #actions>
      <Button variant="solid" :label="__('Cancel')" @click="showDeleteModal = false" />
      <Button variant="solid" theme="red" :label="__('Delete')" :loading="deleting" @click="confirmDelete" />
    </template>
  </Dialog>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { Breadcrumbs, Button, Spinner, Badge, Dialog, FormControl } from 'frappe-ui'
import LayoutHeader from '@/components/LayoutHeader.vue'
import ContactsIcon from '@/components/Icons/ContactsIcon.vue'
import Link from '@/components/Controls/Link.vue'
import { createResource } from 'frappe-ui'

const showCreateModal = ref(false)
const showEditModal = ref(false)
const showDeleteModal = ref(false)

const creating = ref(false)
const updating = ref(false)
const deleting = ref(false)

const selectedStudent = ref(null)

const createFormData = reactive({
  student_name: '',
  email: '',
  phone: '',
  course: '',
  teacher: '',
  organization: '',
  status: 'Active'
})

const editFormData = reactive({
  student_name: '',
  email: '',
  phone: '',
  course: '',
  teacher: '',
  organization: '',
  status: 'Active'
})

const students = createResource({
  url: 'frappe.client.get_list',
  params: {
    doctype: 'CRM Student',
    fields: ['name', 'student_name', 'email', 'phone', 'course', 'teacher', 'organization', 'status'],
    limit: 100
  },
  auto: true
})

const studentsList = computed(() => students.data || [])

function editStudent(student) {
  selectedStudent.value = student

  editFormData.student_name = student.student_name
  editFormData.email = student.email
  editFormData.phone = student.phone || ''
  editFormData.course = student.course || ''
  editFormData.teacher = student.teacher || ''
  editFormData.organization = student.organization || ''
  editFormData.status = student.status || 'Active'

  showEditModal.value = true
}

// Open delete confirmation
function deleteStudent(student) {
  selectedStudent.value = student
  showDeleteModal.value = true
}

// Create new student
async function createStudent() {
  creating.value = true

  try {
    await createResource({
      url: 'frappe.client.insert',
      params: {
        doc: {
          doctype: 'CRM Student',
          ...createFormData
        }
      }
    }).submit()

    await students.reload()
    closeCreateModal()
  } catch (error) {
    console.error('Error creating student:', error)
  } finally {
    creating.value = false
  }
}

// Update existing student
async function updateStudent() {
  updating.value = true

  try {
    await createResource({
      url: 'frappe.client.set_value',
      params: {
        doctype: 'CRM Student',
        name: selectedStudent.value.name,
        fieldname: editFormData
      }
    }).submit()

    await students.reload()
    closeEditModal()
  } catch (error) {
    console.error('Error updating student:', error)
  } finally {
    updating.value = false
  }
}

async function confirmDelete() {
  deleting.value = true

  try {
    await createResource({
      url: 'frappe.client.delete',
      params: {
        doctype: 'CRM Student',
        name: selectedStudent.value.name
      }
    }).submit()

    await students.reload()
    showDeleteModal.value = false
  } catch (error) {
    console.error('Error deleting student:', error)
  } finally {
    deleting.value = false
  }
}

// Close create modal and reset form
function closeCreateModal() {
  showCreateModal.value = false

  // Reset create form
  createFormData.student_name = ''
  createFormData.email = ''
  createFormData.phone = ''
  createFormData.course = ''
  createFormData.teacher = ''
  createFormData.organization = ''
  createFormData.status = 'Active'
}

// Close edit modal and reset form
function closeEditModal() {
  showEditModal.value = false
  selectedStudent.value = null

  // Reset edit form
  editFormData.student_name = ''
  editFormData.email = ''
  editFormData.phone = ''
  editFormData.course = ''
  editFormData.teacher = ''
  editFormData.organization = ''
  editFormData.status = 'Active'
}
</script>