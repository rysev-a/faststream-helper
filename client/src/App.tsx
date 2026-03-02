import { useCallback, useState } from 'react'
import { v4 } from 'uuid'

export interface ProjectType {
  id: string;
  name: string;
  description: string;
}

function App() {
  const [projects, setProjects] = useState<ProjectType[]>([])
  const [correlationID, setCorrelationID] = useState<string | null>(null)


  const loadProjects = useCallback(() => {
    const loadCorrelationID = v4();
    setCorrelationID(loadCorrelationID)

    fetch('/api/projects/10', {
      headers: {
        'correlation-id': loadCorrelationID
      }
    }).then((response) => response.json()).then((data) => {
      setProjects(data.projects)
    })
  }, []);

  return (
    <main>
      <h1>projects</h1>
      {correlationID && <div>correlationID: {correlationID}</div>}
      {projects.map((project) => {
        return <div key={project.id}>{project.id.slice(0, 4)} {project.name} - {project.description}</div>
      })}
      <div>
        <button onClick={loadProjects}>load projects</button>
      </div>
    </main>
  )
}

export default App
