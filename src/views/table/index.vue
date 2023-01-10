<template>
  <div class="app-container">
    <el-table
      v-loading="listLoading"
      :data="list"
      element-loading-text="Loading"
      border
      fit
      highlight-current-row
    >
      <el-table-column align="center" label="ID" width="95">
        <template slot-scope="scope">
          {{ scope.$index }}
        </template>
      </el-table-column>
      <el-table-column label="URL">
        <template slot-scope="scope">
          {{ scope.row.url }}
        </template>
      </el-table-column>
      <el-table-column label="Username" width="110" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.username }}</span>
        </template>
      </el-table-column>
      <el-table-column label="Admin" width="110" align="center">
        <template slot-scope="scope">
          {{ scope.row.is_staff }}
        </template>
      </el-table-column>
      <!-- <el-table-column class-name="status-col" label="Status" width="110" align="center">
        <template slot-scope="scope">
          <el-tag :type="scope.row.status | statusFilter">{{ scope.row.status }}</el-tag>
        </template>
      </el-table-column> -->
      <el-table-column align="center" prop="Email" label="Display_time" width="200">
        <template slot-scope="scope">
          <!-- <i class="el-icon-time" /> -->
          <span>{{ scope.row.email }}</span>
        </template>
      </el-table-column>
    </el-table>

    <br/>

    <el-table
      v-loading="booksListLoading"
      :data="booksList"
      element-loading-text="Loading"
      border
      fit
      highlight-current-row
    >
      <el-table-column align="center" label="ID" width="95">
        <template slot-scope="scope">
          {{ scope.$index }}
        </template>
      </el-table-column>
      <el-table-column label="NAME">
        <template slot-scope="scope">
          {{ scope.row.name }}
        </template>
      </el-table-column>
      <el-table-column label="AUTHER" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.auther }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作">
        
        <template slot-scope="scope">
          <el-button @click="" type="text" size="small">查看</el-button>
          <el-button @click="" type="text" size="small">编辑</el-button>
          <el-button @click="deleteBook(scope.row.id)" type="text" size="small">删除</el-button>
          &npar;
          <!-- <el-popover
            placement="top"
            width="160"
            >
            <p>这是一段内容这是一段内容确定删除吗？</p>
            <div style="text-align: right; margin: 0">
              <el-button size="mini" type="text" >取消</el-button>
              <el-button type="primary" size="mini" >确定</el-button>
            </div>
            <el-button slot="reference">删除</el-button>
          </el-popover> -->
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { getList, getBooksList, delBooks } from '@/api/table'

export default {
  filters: {
    statusFilter(status) {
      const statusMap = {
        published: 'success',
        draft: 'gray',
        deleted: 'danger'
      }
      return statusMap[status]
    }
  },
  data() {
    return {
      list: null,
      listLoading: true,
      booksList: null,
      booksListLoading: true,
      visible: false
    }
  },
  created() {
    this.fetchData()
    this.fetchBooksData()
  },
  methods: {
    fetchData() {
      this.listLoading = true
      getList().then(response => {
        this.list = response
        this.listLoading = false
      })
    },
    fetchBooksData() {
      this.booksListLoading = true
      getBooksList().then(response => {
        this.booksList = response
        this.booksListLoading = false
      })
    },
    deleteBook(id) {
      delBooks(id).then(() => {
          console.log("删除成功", id)
          this.visible = false
          this.booksList.forEach((element,i) => {
            if (element.id == id) {
              this.booksList.splice(i,1)
            }
          });
        }
      )
    }
  }
}
</script>
