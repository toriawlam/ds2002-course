# Milestone 1

1. Choose a name for your team.
   
2. Create a public GitHub repository for your project

   a. Add README.md. For now just add a header with the title. For Milestone, see [How to write a README](how-to-write-a-readme.md).

   b. Add a `LICENSE` file (for example `LICENSE` or `LICENSE.md`). To make software meaningfully open source, your GitHub repository should include a license that describes permissible use. I recommend MIT, but see [GitHub’s guide to licensing a repository](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository#disclaimer) if you want other options.

3. Write a design plan:
   
   Review the high-level schematic of your chosen project (see project subfolders). Create a PDF file with the following sections: 
   
   **Team name:**

   **Team members:**
   
   **Project:** A/B/C

   a. Data Structures 
   - List **input file types** and their sources 
   - List **output file types** 
   - Describe structure of (meta)data records your pipeline will process/write to database(s). You can do this in table format (for SQL DBs) or JSON (for NoSQL) DBs. 
   
   Example SQL:
   | Field | Type | Example |
   | --- | --- | --- |
   | Status | VARCHAR(25) | "SUCCESS" |
   | Created | DATETIME | 2026-04-10 14:31:19 |
   | ... | ... | ... | ... |
   
   Think about appropriate normalization. If you're setting up multiple tables, describe each separately.

   Example NoSQL:
   ```json
   {
      "Status": "OK",
      "Created": "2026-04-10T14:31:19Z",
      ...
   }
   ```

   If you're setting up multiple collections, describe each separately.

   b. Describe which specific systems will be used at each step of your pipeline: 
   - **storage systems:** local, AWS S3, UVA HPC home, UVA HPC scratch, etc?
   - **compute platform:** AWS EC2, AWS serverless, UVA HPC, etc?
   - **database systems:** MySQL, NoSQL, etc?

4. Add your design plan PDF to your GitHub repository.
    
5. Submit your plan

   Submit the link to your project GitHub repo in Canvas.

6. Review approach with instructor

   We will check in with each group in class to confirm your approach and answer questions about your design choices. The date will be shared in class and on Canvas. 




